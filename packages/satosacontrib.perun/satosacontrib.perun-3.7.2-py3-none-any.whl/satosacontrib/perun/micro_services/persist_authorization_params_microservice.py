import logging
from satosa.context import Context
from satosa.internal import InternalData
from satosa.micro_services.base import RequestMicroService

logger = logging.getLogger(__name__)


class PersistAuthorizationParams(RequestMicroService):
    """
    This Satosa microservice picks configured properties from request
    and stores them to context's state under 'persisted_auth_params' property.
    """

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("PersistAuthorizationParams is active")

        self.attributes_to_store = config.get(
            "attributes_to_store", ["session_started_with"]
        )

    def process(self, context: Context, data: InternalData):
        #  For GET methods
        qs_params = context.qs_params
        for attr_name in self.attributes_to_store:
            if qs_params and attr_name in qs_params:
                if context.state.get("persisted_auth_params") is None:
                    context.state["persisted_auth_params"] = {}
                context.state["persisted_auth_params"][attr_name] = qs_params[attr_name]

        # For POST methods
        for attr_name in self.attributes_to_store:
            if context.request and attr_name in context.request:
                if context.state.get("persisted_auth_params") is None:
                    context.state["persisted_auth_params"] = {}
                context.state["persisted_auth_params"][attr_name] = context.request[
                    attr_name
                ]

        return super().process(context, data)
