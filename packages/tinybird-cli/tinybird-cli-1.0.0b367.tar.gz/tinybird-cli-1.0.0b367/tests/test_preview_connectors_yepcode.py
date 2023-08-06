import json
from unittest.mock import patch, AsyncMock, MagicMock
import tornado.testing
from .views.base_test import BaseTest

from tinybird.views.api_errors.data_connectors import PreviewConnectorError
from tinybird.ingest.preview_connectors.yepcode_utils import (
    get_error_message,
    get_available_connectors,
    get_connector_details,
    get_preview,
    create_connector,
    get_executions,
    get_execution_details,
    trigger_execution,
    remove_datasource,
    BASE_URI,
    BASE_HEADERS,
    DATA_CONNECTORS,
    TB_ENDPOINT,
    DATASOURCES_ENDPOINT,
    AVAILABLE_CONNECTORS_ENDPOINT,
    GET_CONNECTOR_DETAILS_ENDPOINT,
    GET_PREVIEW_ENDPOINT,
    CREATE_CONNECTOR_ENDPOINT,
    GET_EXECUTIONS_ENDPOINT,
    GET_EXECUTION_DETAILS_ENDPOINT,
    TRIGGER_EXECUTION_ENDPOINT,
    REMOVE_DATASOURCE_ENDPOINT,
)


class TestYepcodePreviewConnectors(BaseTest):
    def test_get_error_message_response_body(self):
        http_response = MagicMock()
        http_response.error = None
        http_response.body = json.dumps({"error": {'message': "Wadus"}}).encode("utf-8")

        error_message = get_error_message(http_response)
        self.assertEqual(error_message, "Wadus")

    def test_get_error_message_response_error(self):
        http_response = MagicMock()
        http_response.body = None
        http_response.error = json.dumps({"error": "Wadus"}).encode("utf-8")

        error_message = get_error_message(http_response)
        self.assertEqual(error_message, "Wadus")

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        new_callable=AsyncMock,
    )
    async def test_get_available_connectors_ok(self, _requests_mock):
        _ = await get_available_connectors()

        _requests_mock.assert_called_with(
            f"{BASE_URI}{AVAILABLE_CONNECTORS_ENDPOINT}",
            headers=BASE_HEADERS,
            method="GET",
            request_timeout=3600.0,
        )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        side_effect=Exception("Wadus"),
    )
    async def test_get_available_connectors_error(self, _):
        result = await get_available_connectors()

        self.assertEqual(
            result, {"error": PreviewConnectorError.connection_error().message}
        )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        new_callable=AsyncMock,
    )
    async def test_get_connector_details_ok(self, _requests_mock):
        for connector, connector_name in DATA_CONNECTORS.items():
            _ = await get_connector_details(connector=connector)

            _requests_mock.assert_called_with(
                f"{BASE_URI}{GET_CONNECTOR_DETAILS_ENDPOINT}?connector={connector_name}",
                headers=BASE_HEADERS,
                method="GET",
                request_timeout=3600.0,
            )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        side_effect=Exception("Wadus"),
    )
    async def test_get_connector_details_error(self, _):
        for connector, _ in DATA_CONNECTORS.items():
            result = await get_connector_details(connector=connector)

            self.assertEqual(
                result, {"error": PreviewConnectorError.connection_error().message}
            )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        new_callable=AsyncMock,
    )
    async def test_get_preview_endpoint_ok(self, _requests_mock):
        headers = {
            "accept": "application/json",
        }
        zone_id = "myzoneid"
        credentials = {"mycredential": "mysecret"}
        params = {"myparam": "myvalue"}

        for connector, connector_name in DATA_CONNECTORS.items():
            _ = await get_preview(
                connector=connector,
                credentials=credentials,
                params=params,
                zone_id=zone_id,
            )

            body = {
                "zoneId": zone_id,
                "connector": connector_name,
                "credentials": credentials,
                "params": params,
            }

            _requests_mock.assert_called_with(
                f"{BASE_URI}{GET_PREVIEW_ENDPOINT}",
                headers=BASE_HEADERS | headers,
                body=json.dumps(body).encode("utf-8"),
                method="POST",
                request_timeout=3600.0,
                raise_error=False
            )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        side_effect=Exception("Wadus"),
    )
    async def test_get_preview_endpoint_error(self, _):
        zone_id = "myzoneid"
        credentials = {"mycredential": "mysecret"}
        params = {"myparam": "myvalue"}

        for connector, _ in DATA_CONNECTORS.items():
            result = await get_preview(
                connector=connector,
                credentials=credentials,
                params=params,
                zone_id=zone_id,
            )

            self.assertEqual(
                result, {"error": PreviewConnectorError.connection_error().message}
            )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        new_callable=AsyncMock,
    )
    async def test_create_connector_ok(self, _requests_mock):
        tb_token = "myfaketoken"
        zone_id = "myzoneid"
        workspace_id = "myworkspace"
        datasource_id = "mydatasource"
        cron = "0,30 * * * *"
        credentials = {"mycredential": "mysecret"}
        params = {"myparam": "myvalue"}

        for connector, connector_name in DATA_CONNECTORS.items():
            _ = await create_connector(
                connector=connector,
                tb_token=tb_token,
                zone_id=zone_id,
                workspace_id=workspace_id,
                datasource_id=datasource_id,
                cron=cron,
                credentials=credentials,
                params=params,
            )

            body = {
                "zoneId": zone_id,
                "ingestionEndpoint": f"https://{TB_ENDPOINT}{DATASOURCES_ENDPOINT}",
                "ingestionDomain": TB_ENDPOINT,
                "workspace": workspace_id,
                "datasource": datasource_id,
                "apiToken": tb_token,
                "connector": connector_name,
                "cron": cron,
                "credentials": credentials,
                "params": params,
            }

            _requests_mock.assert_called_with(
                f"{BASE_URI}{CREATE_CONNECTOR_ENDPOINT}",
                headers=BASE_HEADERS,
                body=json.dumps(body).encode("utf-8"),
                method="POST",
                request_timeout=3600.0,
            )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        side_effect=Exception("Wadus"),
    )
    async def test_create_connector_error(self, _):
        tb_token = "myfaketoken"
        zone_id = "myzoneid"
        workspace_id = "myworkspace"
        datasource_id = "mydatasource"
        cron = "0,30 * * * *"
        credentials = {"mycredential": "mysecret"}
        params = {"myparam": "myvalue"}

        for connector, _ in DATA_CONNECTORS.items():
            result = await create_connector(
                connector=connector,
                tb_token=tb_token,
                zone_id=zone_id,
                workspace_id=workspace_id,
                datasource_id=datasource_id,
                cron=cron,
                credentials=credentials,
                params=params,
            )

            self.assertEqual(
                result, {"error": PreviewConnectorError.connection_error().message}
            )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        new_callable=AsyncMock,
    )
    async def test_get_executions_ok(self, _requests_mock):
        workspace_id = "myworkspace"
        datasource_id = "mydatasource"

        _ = await get_executions(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
        )

        body = {
            "workspace": workspace_id,
            "datasource": datasource_id,
        }

        _requests_mock.assert_called_with(
            f"{BASE_URI}{GET_EXECUTIONS_ENDPOINT}",
            headers=BASE_HEADERS,
            body=json.dumps(body).encode("utf-8"),
            method="POST",
            request_timeout=3600.0,
        )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        side_effect=Exception("Wadus"),
    )
    async def test_get_executions_error(self, _):
        workspace_id = "myworkspace"
        datasource_id = "mydatasource"

        result = await get_executions(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
        )

        self.assertEqual(
            result, {"error": PreviewConnectorError.connection_error().message}
        )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        new_callable=AsyncMock,
    )
    async def test_get_execution_details_ok(self, _requests_mock):
        workspace_id = "myworkspace"
        datasource_id = "mydatasource"
        execution_id = "myexecution"

        _ = await get_execution_details(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
            execution_id=execution_id,
        )

        body = {
            "workspace": workspace_id,
            "datasource": datasource_id,
            "executionId": execution_id,
        }

        _requests_mock.assert_called_with(
            f"{BASE_URI}{GET_EXECUTION_DETAILS_ENDPOINT}",
            headers=BASE_HEADERS,
            body=json.dumps(body).encode("utf-8"),
            method="POST",
            request_timeout=3600.0,
        )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        side_effect=Exception("Wadus"),
    )
    async def test_get_execution_details_error(self, _):
        workspace_id = "myworkspace"
        datasource_id = "mydatasource"
        execution_id = "myexecution"

        result = await get_execution_details(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
            execution_id=execution_id,
        )

        self.assertEqual(
            result, {"error": PreviewConnectorError.connection_error().message}
        )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        new_callable=AsyncMock,
    )
    async def test_trigger_execution_ok(self, _requests_mock):
        workspace_id = "myworkspace"
        datasource_id = "mydatasource"

        _ = await trigger_execution(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
        )

        body = {
            "workspace": workspace_id,
            "datasource": datasource_id,
        }

        _requests_mock.assert_called_with(
            f"{BASE_URI}{TRIGGER_EXECUTION_ENDPOINT}",
            headers=BASE_HEADERS,
            body=json.dumps(body).encode("utf-8"),
            method="POST",
            request_timeout=3600.0,
        )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        side_effect=Exception("Wadus"),
    )
    async def test_trigger_execution_error(self, _):
        workspace_id = "myworkspace"
        datasource_id = "mydatasource"

        result = await trigger_execution(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
        )

        self.assertEqual(
            result, {"error": PreviewConnectorError.connection_error().message}
        )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        new_callable=AsyncMock,
    )
    async def test_remove_datasource_ok(self, _requests_mock):
        workspace_id = "myworkspace"
        datasource_id = "mydatasource"

        _ = await remove_datasource(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
        )

        body = {
            "workspace": workspace_id,
            "datasource": datasource_id,
        }

        _requests_mock.assert_called_with(
            f"{BASE_URI}{REMOVE_DATASOURCE_ENDPOINT}",
            headers=BASE_HEADERS,
            body=json.dumps(body).encode("utf-8"),
            method="POST",
            request_timeout=3600.0,
        )

    @tornado.testing.gen_test
    @patch(
        "tinybird.ingest.preview_connectors.yepcode_utils.http_client.fetch",
        side_effect=Exception("Wadus"),
    )
    async def test_remove_datasource_error(self, _):
        workspace_id = "myworkspace"
        datasource_id = "mydatasource"

        result = await remove_datasource(
            workspace_id=workspace_id,
            datasource_id=datasource_id,
        )

        self.assertEqual(
            result, {"error": PreviewConnectorError.connection_error().message}
        )
