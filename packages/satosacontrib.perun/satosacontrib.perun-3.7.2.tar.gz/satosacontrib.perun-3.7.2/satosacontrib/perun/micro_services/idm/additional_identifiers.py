import json
import re
from typing import List, Dict

from perun.connector import AdaptersManager, Logger
from perun.connector.adapters.AdaptersManager import AdaptersManagerNotExistsException
from satosa.context import Context
from satosa.exception import SATOSAError
from satosa.internal import InternalData
from satosa.micro_services.base import ResponseMicroService
from satosa.response import Redirect

from satosacontrib.perun.utils.Utils import Utils

from satosacontrib.perun.utils.ConfigStore import ConfigStore


class AdditionalIdentifiers(ResponseMicroService):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__logger = Logger.get_logger(self.__class__.__name__)

        self.__global_cfg = ConfigStore.get_global_cfg(config["global_cfg_path"])
        self.__attr_map_cfg = ConfigStore.get_attributes_map(
            self.__global_cfg["attrs_cfg_path"]
        )
        self.__adapters_manager = AdaptersManager(
            self.__global_cfg["adapters_manager"], self.__attr_map_cfg
        )

        hash_fun_name = config.get("hash_func", None)
        self.__hash_func = None
        self.__hash_Salt = config.get("hash_salt", "")
        if hash_fun_name:
            self.__hash_func = Utils.get_hash_function(hash_fun_name)

        self.__perun_user_id_attr = self.__global_cfg["perun_user_id_attribute"]
        self.__perun_login_attribute = self.__global_cfg["perun_login_attribute"]
        self.__identifiers_attribute = config["identifiers_attribute"]
        self.__main_identifier_attribute = config["main_identifier_attribute"]
        self.__internal_extsource_attribute = config["internal_extsource_attribute"]
        self.__proxy_extsource_name = config["proxy_extsource_name"]
        self.__prefix_for_removal = config.get("prefix_for_removal", None)
        self.__hash_attributes = config.get("hash_attributes")
        self.__registration_page_url = config.get("registration_page_url", "")
        self.__registration_result_url = config.get("registration_result_url", "")
        self.__lack_of_attributes_url = config["lack_of_attributes_url"]
        self.__endpoint = "/process"
        self.__signing_cfg = self.__global_cfg["jwk"]
        self.__allowed_requesters = self.__global_cfg.get("allowed_requesters", {})

    def __handle_registration_response(self, context: Context):
        """
        Handles response from external service with the result of new user
        registration.

        @param context: request context
        @return: loaded newly registered user if registration was successful
        """
        context, data = Utils.handle_registration_response(
            context, self.__signing_cfg, self.__registration_result_url, self.name
        )
        return self.process(context, data)

    def process(self, context, data):
        """
        :param context: request context
        :param data: the internal request
        """

        if not Utils.allow_by_requester(context, data, self.__allowed_requesters):
            return super().process(context, data)

        attr_values_to_hash = self.get_attributes_values_to_hash(data)

        if not attr_values_to_hash:
            return Redirect(self.__lack_of_attributes_url)

        hashed_attr_values = []
        for val_to_hash in attr_values_to_hash:
            val_to_hash += self.__hash_Salt
            if self.__hash_func:
                val_to_hash = self.__hash_func(val_to_hash.encode("utf-8")).hexdigest()
            hashed_attr_values.append(val_to_hash)

        method = self.__adapters_manager.get_user_ext_source_by_unique_attribute_value
        try:
            ues = method(self.__identifiers_attribute, hashed_attr_values)
        except AdaptersManagerNotExistsException:
            not_exists = True

            if self.__prefix_for_removal:
                try:
                    ues = method(
                        self.__identifiers_attribute,
                        [
                            self.__prefix_for_removal + value
                            for value in attr_values_to_hash
                        ],
                    )
                    not_exists = False
                except AdaptersManagerNotExistsException:
                    pass

            if not_exists:
                if not self.__registration_page_url:
                    raise SATOSAError(
                        f"User with attributes '{attr_values_to_hash}' was not "
                        "found in Perun. And redirect link to registration "
                        "page is missing in the config file."
                    )
                return self.handle_user_not_found(context, data)

        ues_attrs = self.__adapters_manager.get_user_ext_source_attributes(
            ues.id, [self.__main_identifier_attribute, self.__identifiers_attribute]
        )

        updated_hashes = list(
            set(ues_attrs.get(self.__identifiers_attribute) + hashed_attr_values)
        )

        if self.__prefix_for_removal:
            updated_hashes = [
                val
                for val in updated_hashes
                if not re.match(rf"^{self.__prefix_for_removal}", val)
            ]

        data.attributes[self.__identifiers_attribute] = updated_hashes
        data.subject_id = ues_attrs.get(self.__main_identifier_attribute)
        data.attributes[self.__main_identifier_attribute] = ues_attrs.get(
            self.__main_identifier_attribute
        )
        data.attributes[self.__perun_user_id_attr] = ues.user.id
        data.attributes[self.__internal_extsource_attribute] = [
            self.__proxy_extsource_name
        ]

        return super().process(context, data)

    @staticmethod
    def __build_value_to_hash(data: InternalData, attribute_cfg: Dict[str, str]) -> str:
        to_hash = []
        for attr_name, regex in attribute_cfg.items():
            if attr_name == "requester":
                attribute_values = [data.requester]
            else:
                attribute_values = data.attributes.get(attr_name)
            if attribute_values:
                cur_value = []
                if isinstance(attribute_values, list):
                    for attr_val in attribute_values:
                        if re.search(regex, attr_val):
                            cur_value.append(attr_val)
                    if not cur_value:
                        return ""
                    to_hash.append(cur_value)
                else:
                    if re.search(regex, attribute_values):
                        cur_value.append(attribute_values)
                    if not cur_value:
                        return ""
                    to_hash.append(cur_value)
            else:
                return ""
        if not to_hash:
            return ""
        return json.dumps(to_hash)

    def get_attributes_values_to_hash(self, data: InternalData) -> List[str]:
        result_attr_values = []
        for attribute_cfg in self.__hash_attributes:
            value_to_hash = self.__build_value_to_hash(data, attribute_cfg)
            if value_to_hash:
                result_attr_values.append(value_to_hash)
        return result_attr_values

    def handle_user_not_found(self, context: Context, data: InternalData) -> Redirect:
        """
        Handles a case when user we were looking for wasn't found in the
        external system. Redirects user to a registration page if possible,
        otherwise raises SATOSAError.

        @param context: request context
        @param data: the internal request
        @return: redirect to registration page
        """

        request_data = {}
        return Utils.secure_redirect_with_nonce(
            context,
            data,
            request_data,
            self.__registration_page_url,
            self.__signing_cfg,
            self.name,
        )

    def register_endpoints(self):
        """
        Registers an endpoint for external service reply when looking for
        user's credentials.

        @return: url of endpoint for external service to reply to and a method
                 to handle the reply
        """
        return [
            (f"^perunuserhashed{self.__endpoint}$", self.__handle_registration_response)
        ]
