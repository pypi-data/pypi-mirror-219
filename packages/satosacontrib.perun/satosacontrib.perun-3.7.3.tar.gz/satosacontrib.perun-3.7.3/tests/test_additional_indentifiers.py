import copy
import hashlib
import logging
from unittest.mock import patch, MagicMock

from perun.connector import AdaptersManager, UserExtSource, User
from perun.connector.adapters.AdaptersManager import AdaptersManagerNotExistsException
from satosa.internal import InternalData
from satosa.micro_services.base import MicroService

from satosacontrib.perun.micro_services.idm import AdditionalIdentifiers
from tests.test_microservice_loader import Loader, TestContext

MICROSERVICE_CONFIG = {
    "global_cfg_path": "example_path",
    "internal_extsource_attribute": "example_internal_extsource",
    "proxy_extsource_name": "example_extsource_name",
    "registration_page_url": "example_url",
    "registration_result_url": "example_url",
    "lack_of_attributes_url": "example_url",
    "hash_attributes": [
        {"eppn": ".+", "eduPersonAssurance": "no-eppn-reassign"},
        {"epuid": ".+"},
        {
            "givenName": ".+",
            "sn": ".+",
            "requester": "http://incompetent-idp.example.com",
        },
        {
            "cn": ".+",
            "requester": "http://incompetent-idp.example.com",
        },
    ],
    "hash_func": "sha512",
    "hash_salt": "example_salt",
    "identifiers_attribute": "additionalIdentifiers",
    "main_identifier_attribute": "persitentId",
    "prefix_for_removal": "",
}

MICROSERVICE = Loader(
    MICROSERVICE_CONFIG, "AdditionalIdentifiers"
).create_mocked_instance(perun_micro_service=True)


@patch("satosa.context.Context.get_decoration")
def test_process_requester_not_allowed(mock_method, caplog):
    mock_method.return_value = "target_entity_id2"
    data_with_disallowed_requester = InternalData()
    data_with_disallowed_requester.requester = "forbidden_requester"
    disallowed_requester_log = "Requester 'forbidden_requester' is not allowed for 'target_entity_id2' due to deny rules"
    MicroService.process = MagicMock(return_value=None)
    with caplog.at_level(logging.DEBUG):
        MICROSERVICE.process(TestContext(), data_with_disallowed_requester)
        assert disallowed_requester_log in caplog.text
        MicroService.process.assert_called()


@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager.get_user_ext_source_by_unique_attribute_value"
)
@patch(
    "satosacontrib.perun.micro_services.idm.additional_identifiers.AdditionalIdentifiers.handle_user_not_found"  # noqa
)
def test_process_user_not_found(mock_request_1, mock_request_2):
    internal_data = InternalData()
    internal_data.requester = "allowed_req_1"
    internal_data.auth_info.issuer = "example_non_existent_name"
    internal_data.attributes = {"epuid": "value1", "eppn": "value2"}

    AdaptersManager.get_user_ext_source_by_unique_attribute_value = MagicMock(
        side_effect=AdaptersManagerNotExistsException(
            '"name":"UserExtSourceNotExistsException"'
        )
    )
    AdditionalIdentifiers.handle_user_not_found = MagicMock(return_value=None)
    MICROSERVICE.process(TestContext(), internal_data)
    AdditionalIdentifiers.handle_user_not_found.assert_called_once()


@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager.get_user_ext_source_by_unique_attribute_value"
)
@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager.get_user_ext_source_attributes"
)
@patch("satosa.micro_services.base.MicroService.process")
def test_old_prefix(mock_request_1, mock_request_2, mock_request_3):
    internal_data = InternalData()
    internal_data.requester = "allowed_req_1"
    internal_data.auth_info.issuer = "example_non_existent_name"
    internal_data.attributes = {"epuid": "value1", "eppn": "value2"}

    config_with_old_prefix = copy.deepcopy(MICROSERVICE_CONFIG)
    config_with_old_prefix["prefix_for_removal"] = "old-"
    microservice = Loader(
        config_with_old_prefix, "AdditionalIdentifiers"
    ).create_mocked_instance(perun_micro_service=True)

    AdaptersManager.get_user_ext_source_by_unique_attribute_value = MagicMock(
        side_effect=[
            AdaptersManagerNotExistsException(
                '"name":"UserExtSourceNotExistsException"'
            ),
            UserExtSource(
                1, "example_ext_src", "example_login", User(1, "example_name")
            ),
        ]
    )

    result_hash = hashlib.sha512('[["value1"]]example_salt'.encode("utf-8")).hexdigest()

    AdaptersManager.get_user_ext_source_attributes = MagicMock(
        return_value={
            "persitentId": "id1",
            "additionalIdentifiers": ['old-[["value1"]]'],
        }
    )
    MicroService.process = MagicMock(return_value=None)

    microservice.process(TestContext(), internal_data)
    assert internal_data.attributes["persitentId"] == "id1"
    assert internal_data.attributes["additionalIdentifiers"] == [result_hash]


@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager.get_user_ext_source_by_unique_attribute_value"
)
@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager.get_user_ext_source_attributes"
)
@patch("satosa.micro_services.base.MicroService.process")
def test_add_new_hash(mock_request_1, mock_request_2, mock_request_3):
    internal_data = InternalData()
    internal_data.requester = "allowed_req_1"
    internal_data.auth_info.issuer = "example_non_existent_name"
    internal_data.attributes = {"epuid": "value2", "eppn": "dummy"}

    microservice = Loader(
        MICROSERVICE_CONFIG, "AdditionalIdentifiers"
    ).create_mocked_instance(perun_micro_service=True)

    AdaptersManager.get_user_ext_source_by_unique_attribute_value = MagicMock(
        return_value=UserExtSource(
            1, "example_ext_src", "example_login", User(1, "example_name")
        ),
    )

    result_hash1 = hashlib.sha512(
        '[["value1"]]example_salt'.encode("utf-8")
    ).hexdigest()
    result_hash2 = hashlib.sha512(
        '[["value2"]]example_salt'.encode("utf-8")
    ).hexdigest()

    AdaptersManager.get_user_ext_source_attributes = MagicMock(
        return_value={
            "persitentId": "id1",
            "additionalIdentifiers": [result_hash1],
        }
    )
    MicroService.process = MagicMock(return_value=None)

    microservice.process(TestContext(), internal_data)
    assert internal_data.attributes["persitentId"] == "id1"
    additionalIdentifiers = internal_data.attributes["additionalIdentifiers"]
    assert len(additionalIdentifiers) == 2
    assert result_hash1 in additionalIdentifiers
    assert result_hash2 in additionalIdentifiers


def test_hash_attributes_no_match():
    internal_data = InternalData()
    internal_data.requester = "allowed_req_1"
    internal_data.auth_info.issuer = "example_non_existent_name"
    internal_data.attributes = {"eppn": "value1", "givenName": "John"}

    microservice = Loader(
        MICROSERVICE_CONFIG, "AdditionalIdentifiers"
    ).create_mocked_instance(perun_micro_service=True)
    result = microservice.process(TestContext(), internal_data)
    assert result.message == "example_url"


@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager.get_user_ext_source_by_unique_attribute_value"
)
@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager.get_user_ext_source_attributes"
)
@patch("satosa.micro_services.base.MicroService.process")
def test_hash_attributes_eppn_eduPersonAssurance(
    mock_request_1, mock_request_2, mock_request_3
):
    internal_data = InternalData()
    internal_data.requester = "allowed_req_1"
    internal_data.auth_info.issuer = "example_non_existent_name"
    internal_data.attributes = {
        "eppn": "value1",
        "eduPersonAssurance": ["something", "https://.../no-eppn-reassign"],
    }

    microservice = Loader(
        MICROSERVICE_CONFIG, "AdditionalIdentifiers"
    ).create_mocked_instance(perun_micro_service=True)

    AdaptersManager.get_user_ext_source_by_unique_attribute_value = MagicMock(
        return_value=UserExtSource(
            1, "example_ext_src", "example_login", User(1, "example_name")
        ),
    )

    result_hash = hashlib.sha512(
        '[["value1"], ["https://.../no-eppn-reassign"]]example_salt'.encode("utf-8")
    ).hexdigest()

    AdaptersManager.get_user_ext_source_attributes = MagicMock(
        return_value={
            "persitentId": "id1",
            "additionalIdentifiers": [result_hash],
        }
    )
    MicroService.process = MagicMock(return_value=None)

    microservice.process(TestContext(), internal_data)
    assert internal_data.attributes["persitentId"] == "id1"
    additionalIdentifiers = internal_data.attributes["additionalIdentifiers"]
    assert len(additionalIdentifiers) == 1
    assert result_hash in additionalIdentifiers


def test_hash_attributes_not_matching_requester():
    internal_data = InternalData()
    internal_data.auth_info.issuer = "example_non_existent_name"
    internal_data.attributes = {"givenName": "value1", "sn": "something"}
    internal_data.requester = "https://goodidp.example.com"

    microservice = Loader(
        MICROSERVICE_CONFIG, "AdditionalIdentifiers"
    ).create_mocked_instance(perun_micro_service=True)
    result = microservice.process(TestContext(), internal_data)
    assert result.message == "example_url"


@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager.get_user_ext_source_by_unique_attribute_value"
)
@patch(
    "perun.connector.adapters.AdaptersManager.AdaptersManager.get_user_ext_source_attributes"
)
@patch("satosa.micro_services.base.MicroService.process")
def test_hash_attributes_matching_requester(
    mock_request_1, mock_request_2, mock_request_3
):
    internal_data = InternalData()
    internal_data.auth_info.issuer = "example_non_existent_name"
    internal_data.attributes = {"givenName": "value1", "sn": "something"}
    internal_data.requester = "http://incompetent-idp.example.com"

    microservice = Loader(
        MICROSERVICE_CONFIG, "AdditionalIdentifiers"
    ).create_mocked_instance(perun_micro_service=True)

    AdaptersManager.get_user_ext_source_by_unique_attribute_value = MagicMock(
        return_value=UserExtSource(
            1, "example_ext_src", "example_login", User(1, "example_name")
        ),
    )

    result_hash = hashlib.sha512(
        '[["value1"], ["something"], ["http://incompetent-idp.example.com"]]example_salt'.encode(
            "utf-8"
        )
    ).hexdigest()

    AdaptersManager.get_user_ext_source_attributes = MagicMock(
        return_value={
            "persitentId": "id1",
            "additionalIdentifiers": [result_hash],
        }
    )
    MicroService.process = MagicMock(return_value=None)

    microservice.process(TestContext(), internal_data)
    assert internal_data.attributes["persitentId"] == "id1"
    additionalIdentifiers = internal_data.attributes["additionalIdentifiers"]
    assert len(additionalIdentifiers) == 1
    assert result_hash in additionalIdentifiers
