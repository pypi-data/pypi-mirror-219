import logging
from satosa.context import Context
from satosa.internal import InternalData
from satosa.micro_services.base import ResponseMicroService

logger = logging.getLogger(__name__)


class SessionStartedWith(ResponseMicroService):
    """
    This Satosa microservice checks, if configured attribute's value is present
    in list of persisted auth parameters' "session_started_with" values.
    Attribute typing microservice is expected to run after this microservice to convert
    string value to boolean.
    """

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.LOG_PREFIX = "SessionStartedWith: "
        logger.info("SessionStartedWith is active")

        self.attribute_to_check = config.get("attribute_to_check", "firstrpinsession")
        self.list_name = "session_started_with"
        self.persisted_attrs_name = "persisted_auth_params"
        self.result_attr_name = config.get(
            "result_attr_name", "sessionstartedwithchecked"
        )

    def process(self, context: Context, data: InternalData):
        attr_to_check = data.attributes.get(self.attribute_to_check)
        if attr_to_check is None:
            logger.debug(
                self.LOG_PREFIX + f"Missing {self.attribute_to_check} in user data."
            )
            return super().process(context, data)

        persisted_auth_params = context.state.get(self.persisted_attrs_name)
        if (
            persisted_auth_params is None
            or persisted_auth_params.get(self.list_name) is None
        ):
            logger.debug(
                self.LOG_PREFIX + f"Missing {self.persisted_attrs_name} in state data."
            )
            return super().process(context, data)

        persisted_attr_values = persisted_auth_params[self.list_name].split(" ")
        if attr_to_check in persisted_attr_values:
            data.attributes[self.result_attr_name] = ["true"]
            logger.info(
                self.LOG_PREFIX + f"{attr_to_check} found in {persisted_attr_values}"
            )

        return super().process(context, data)
