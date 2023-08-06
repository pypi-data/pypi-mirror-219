import logging
from satosa.micro_services.base import RequestMicroService

logger = logging.getLogger(__name__)


class AuthSwitcherLiteRequest(RequestMicroService):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("AuthSwitcherLiteRequest is active")

    def process(self, context, data):
        """
        Forward requested ACRs (from frontend) at upstream IdP (backend).
        :param context: request context
        :param data: the internal request
        """

        requested_acrs = context.state.get(
            context.KEY_AUTHN_CONTEXT_CLASS_REF
        ) or context.get_decoration(context.KEY_AUTHN_CONTEXT_CLASS_REF)

        context.decorate(context.KEY_TARGET_AUTHN_CONTEXT_CLASS_REF, requested_acrs)
        context.state[context.KEY_TARGET_AUTHN_CONTEXT_CLASS_REF] = requested_acrs

        return super().process(context, data)
