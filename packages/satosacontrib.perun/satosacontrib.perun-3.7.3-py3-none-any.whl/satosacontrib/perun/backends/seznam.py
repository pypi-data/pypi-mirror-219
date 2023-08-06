"""
Seznam.cz backend module.
"""
import logging
from datetime import datetime
from urllib.parse import urlparse

from oic import oic
from oic import rndstr
from oic.oic.message import AuthorizationResponse
from oic.oic.message import ProviderConfigurationResponse
from oic.oic.message import RegistrationRequest
from oic.utils.authn.authn_context import UNSPECIFIED
from oic.utils.authn.client import CLIENT_AUTHN_METHOD

import satosa.logging_util as lu
from satosa.internal import AuthenticationInformation
from satosa.internal import InternalData
from satosa.backends.base import BackendModule
from satosa.backends.oauth import get_metadata_desc_for_oauth_backend
from satosa.exception import SATOSAAuthenticationError, SATOSAError
from satosa.response import Redirect


logger = logging.getLogger(__name__)

STATE_KEY = "oidc_state"


# https://vyvojari.seznam.cz/oauth/doc
class SeznamBackend(BackendModule):
    """
    Sign in with Seznam.cz backend
    """

    def __init__(self, auth_callback_func, internal_attributes, config, base_url, name):
        super().__init__(auth_callback_func, internal_attributes, base_url, name)
        self.auth_callback_func = auth_callback_func
        self.config = config
        self.client = _create_client(
            config["provider_metadata"],
            config["client"]["client_metadata"],
            config["client"].get("verify_ssl", True),
        )
        if "scope" not in config["client"]["auth_req_params"]:
            config["auth_req_params"]["scope"] = "identity"
        if "response_type" not in config["client"]["auth_req_params"]:
            config["auth_req_params"]["response_type"] = "code"

    def start_auth(self, context, request_info):
        """
        See super class method satosa.backends.base#start_auth
        :type context: satosa.context.Context
        :type request_info: satosa.internal.InternalData
        """
        oidc_state = rndstr()
        state_data = {STATE_KEY: oidc_state}
        context.state[self.name] = state_data

        args = {
            "scope": self.config["client"]["auth_req_params"]["scope"],
            "response_type": self.config["client"]["auth_req_params"]["response_type"],
            "client_id": self.client.client_id,
            "redirect_uri": self.client.registration_response["redirect_uris"][0],
            "state": oidc_state,
        }
        args.update(self.config["client"]["auth_req_params"])
        auth_req = self.client.construct_AuthorizationRequest(request_args=args)
        login_url = auth_req.request(self.client.authorization_endpoint)
        return Redirect(login_url)

    def register_endpoints(self):
        url_map = []
        redirect_path = urlparse(
            self.config["client"]["client_metadata"]["redirect_uris"][0]
        ).path
        if not redirect_path:
            raise SATOSAError("Missing path in redirect uri")

        url_map.append(("^%s$" % redirect_path.lstrip("/"), self.response_endpoint))
        return url_map

    def _get_tokens(self, authn_response, context):
        """
        :param authn_response: authentication response from OP
        :type authn_response: oic.oic.message.AuthorizationResponse
        :return: access token and ID Token claims
        :rtype: Tuple[Optional[str], Optional[Mapping[str, str]]]
        """
        if "code" in authn_response:
            # make token request
            args = {
                "code": authn_response["code"],
                "redirect_uri": self.client.registration_response["redirect_uris"][0],
            }

            token_resp = self.client.do_access_token_request(
                scope="openid",
                state=authn_response["state"],
                request_args=args,
                authn_method=self.client.registration_response[
                    "token_endpoint_auth_method"
                ],
            )

            self._check_error_response(token_resp, context)
            return token_resp.get("access_token"), {
                "account_name": token_resp.get("account_name"),
                "user_id": token_resp.get("user_id"),
            }

        return authn_response.get("access_token"), authn_response.get("id_token")

    def _check_error_response(self, response, context):
        """
        Check if the response is an OAuth error response.
        :param response: the OIDC response
        :type response: oic.oic.message
        :raise SATOSAAuthenticationError: if the response is an OAuth error response
        """
        if "error" in response:
            msg = "{name} error: {error} {description}".format(
                name=type(response).__name__,
                error=response["error"],
                description=response.get("error_description", ""),
            )
            logline = lu.LOG_FMT.format(
                id=lu.get_session_id(context.state), message=msg
            )
            logger.debug(logline)
            raise SATOSAAuthenticationError(context.state, "Access denied")

    def _get_userinfo(self, state, context):
        kwargs = {"method": self.config["client"].get("userinfo_request_method", "GET")}
        userinfo_resp = self.client.do_user_info_request(state=state, **kwargs)
        self._check_error_response(userinfo_resp, context)
        return userinfo_resp.to_dict()

    def response_endpoint(self, context, *args):
        """
        Handles the authentication response from the OP.
        :type context: satosa.context.Context
        :type args: Any
        :rtype: satosa.response.Response

        :param context: SATOSA context
        :param args: None
        :return:
        """
        backend_state = context.state[self.name]
        authn_resp = self.client.parse_response(
            AuthorizationResponse, info=context.request, sformat="dict"
        )
        if backend_state[STATE_KEY] != authn_resp["state"]:
            msg = "Missing or invalid state in authn response for state: {}".format(
                backend_state
            )
            logline = lu.LOG_FMT.format(
                id=lu.get_session_id(context.state), message=msg
            )
            logger.debug(logline)
            raise SATOSAAuthenticationError(
                context.state, "Missing or invalid state in authn response"
            )

        self._check_error_response(authn_resp, context)
        access_token, id_token_claims = self._get_tokens(authn_resp, context)
        if not id_token_claims:
            id_token_claims = {}

        userinfo = {}
        if access_token:
            # make userinfo request
            userinfo = self._get_userinfo(authn_resp["state"], context)

        if not id_token_claims and not userinfo:
            msg = "No id_token or userinfo, nothing to do.."
            logline = lu.LOG_FMT.format(
                id=lu.get_session_id(context.state), message=msg
            )
            logger.error(logline)
            raise SATOSAAuthenticationError(context.state, "No user info available.")

        all_user_claims = dict(list(userinfo.items()) + list(id_token_claims.items()))
        msg = "UserInfo: {}".format(all_user_claims)
        logline = lu.LOG_FMT.format(id=lu.get_session_id(context.state), message=msg)
        logger.debug(logline)
        del context.state[self.name]
        internal_resp = self._translate_response(
            all_user_claims, self.client.authorization_endpoint
        )
        return self.auth_callback_func(context, internal_resp)

    def _translate_response(self, response, issuer):
        """
        Translates oidc response to SATOSA internal response.
        :type response: dict[str, str]
        :type issuer: str
        :type subject_type: str
        :rtype: InternalData

        :param response: Dictioary with attribute name as key.
        :param issuer: The oidc op that gave the repsonse.
        :param subject_type: public or pairwise according to oidc standard.
        :return: A SATOSA internal response.
        """
        auth_info = AuthenticationInformation(UNSPECIFIED, str(datetime.now()), issuer)
        internal_resp = InternalData(auth_info=auth_info)
        internal_resp.attributes = self.converter.to_internal("seznam", response)
        internal_resp.subject_id = response["advert_user_id"]
        return internal_resp

    def get_metadata_desc(self):
        """
        See satosa.backends.oauth.get_metadata_desc
        :rtype: satosa.metadata_creation.description.MetadataDescription
        """
        return get_metadata_desc_for_oauth_backend(
            self.config["provider_metadata"]["issuer"], self.config
        )


def _create_client(provider_metadata, client_metadata, verify_ssl=True):
    """
    Create a pyoidc client instance.
    :param provider_metadata: provider configuration information
    :type provider_metadata: Mapping[str, Union[str, Sequence[str]]]
    :param client_metadata: client metadata
    :type client_metadata: Mapping[str, Union[str, Sequence[str]]]
    :return: client instance to use for communicating with the configured provider
    :rtype: oic.oic.Client
    """
    client = oic.Client(client_authn_method=CLIENT_AUTHN_METHOD, verify_ssl=verify_ssl)

    # Provider configuration information
    if "authorization_endpoint" in provider_metadata:
        # no dynamic discovery necessary
        client.handle_provider_config(
            ProviderConfigurationResponse(**provider_metadata),
            provider_metadata["issuer"],
        )
    else:
        # do dynamic discovery
        client.provider_config(provider_metadata["issuer"])

    # Client information
    if "client_id" in client_metadata:
        # static client info provided
        client.store_registration_info(RegistrationRequest(**client_metadata))
    else:
        # do dynamic registration
        client.register(
            client.provider_info["registration_endpoint"], **client_metadata
        )

    client.subject_type = (
        client.registration_response.get("subject_type")
        or client.provider_info["subject_types_supported"][0]
    )
    return client
