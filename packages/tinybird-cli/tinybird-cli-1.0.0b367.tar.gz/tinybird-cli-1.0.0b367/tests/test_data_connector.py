from io import BytesIO
from urllib.parse import parse_qs
import uuid

import atexit
import os
import sys
from unittest import mock
import tornado.testing
import subprocess
from unittest.mock import AsyncMock, patch
from tornado.httpclient import HTTPRequest, HTTPResponse

from confluent_kafka import Producer

from tinybird.kafka_utils import KafkaServerGroupsConfig, KafkaTbUtils, KafkaUtils, TBAKafkaClient
from .views.base_test import BaseTest
import shutil

from tinybird import data_connector
from tinybird.user import UserAccount, User, Users

KAFKA_PATH = os.environ.get('KAFKA_PATH', os.path.join(os.path.dirname(__file__), '../..', 'kafka_2.13-2.8.0'))


class TestDataConnector(BaseTest):
    @tornado.testing.gen_test
    async def test_raises_exception_if_service_not_supported(self):
        with self.assertRaisesRegex(
            data_connector.InvalidSettingsException,
            "Service connector \(\'\'\) is not supported or does not exist"
        ):
            data_connector.DataConnector.add_connector(
                user=self.base_workspace,
                name="name",
                service='',
                settings={}
            )

        with self.assertRaisesRegex(
            data_connector.InvalidSettingsException,
            "Service connector \(\'unknown\'\) is not supported or does not exist"
        ):
            data_connector.DataConnector.add_connector(
                user=self.base_workspace,
                name="name",
                service='unknown',
                settings={}
            )


class TestKafka(BaseTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        shutil.rmtree('/tmp/kafka-logs-test', ignore_errors=True)
        shutil.rmtree('/tmp/zookeeper-kafka-test', ignore_errors=True)

        args = (
            f'{KAFKA_PATH}/bin/zookeeper-server-start.sh',
            os.path.join(os.path.dirname(__file__), '..', './tests/kafka-zookeeper-test.properties')
        )
        cls.zookeeper_process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=sys.stdout, universal_newlines=True)

        @atexit.register
        def kill_zk():
            cls.zookeeper_process.kill()

        found = False
        while not found:
            if cls.zookeeper_process.poll() is not None:
                break
            for line in iter(cls.zookeeper_process.stdout.readline, ''):
                if line.find('Using checkInterval') != -1:
                    print("ZK started!")
                    found = True
                    break
                if line.find('Unexpected exception') != -1:
                    print("Could not start ZK process: " + line.rstrip())
                    cls.assertTrue(False, None, msg="ZK process not started")
                    return

        args = (
            f'{KAFKA_PATH}/bin/kafka-server-start.sh',
            os.path.join(os.path.dirname(__file__), '..', './tests/kafka-test-server.properties')
        )
        cls.kafka_process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=sys.stdout, universal_newlines=True)

        @atexit.register
        def kill_kafka():
            cls.kafka_process.kill()

        found = False
        while not found:
            if cls.kafka_process.poll() is not None:
                break

            for line in iter(cls.kafka_process.stdout.readline, ''):
                if line.find('Recorded new controller') != -1:
                    print("KAFKA server started : " + line.rstrip())
                    found = True
                    break
                if line.find('Unexpected exception') != -1:
                    print("Could not start Kafka process: " + line.rstrip())
                    cls.assertTrue(False, None, msg="Kafka process not started")
                    return

        cls.zookeeper_process.stdout.close()
        cls.kafka_process.stdout.close()

    def setUp(self):
        super().setUp()
        self.assertEqual(self.zookeeper_process.poll(), None, msg="ZK process could not start")
        self.assertEqual(self.kafka_process.poll(), None, msg="Kafka process could not start")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.kafka_process.kill()
        cls.zookeeper_process.kill()

    def produce_message(self, message, topic, headers=None):
        conf = {
            'bootstrap.servers': 'localhost:9093',
            'security.protocol': 'PLAINTEXT',
            'sasl.mechanism': 'PLAIN',
            'compression.type': 'zstd',
            'compression.level': 8,
            'sasl.username': '',
            'sasl.password': '',
        }
        producer = Producer(conf)

        producer.produce(topic, value=message, headers=headers)
        producer.flush()

    def create_kafka_connector(self):
        user_account = UserAccount.register(f'test_kafka_preview{uuid.uuid4().hex}@mail', 'pass')
        workspace = self.register_workspace(f'test_kafka_preview_ws_{uuid.uuid4().hex}', user_account.id)

        conn = data_connector.DataConnector.add_connector(user=workspace, name="name", service='kafka', settings={
            'kafka_bootstrap_servers': 'localhost:9093',
            'kafka_security_protocol': 'plaintext',
            'kafka_sasl_plain_username': '',
            'kafka_sasl_plain_password': '',
        })

        return conn

    @tornado.testing.gen_test
    @patch('tinybird.data_connector.KafkaSettings.PREVIEW_POLL_TIMEOUT_MS', 2000)
    async def test_kafka_preview_all_params_happy(self):
        self.produce_message('{"test": 3}', "kafkafirst")
        conn = self.create_kafka_connector()
        r = await KafkaUtils.get_kafka_preview(conn,
                                               'test_groupid',
                                               kafka_topics=['kafkafirst'])
        assert r.get('error', None) is None
        output = r['preview']
        expected_deserialization = {
            'data': [{'test': 3}],
            'meta': [{'name': 'test', 'type': 'Int16'}],
            'rows': 1,
            'statistics': mock.ANY
        }
        self.assertEqual(len(output), 1)
        t = output[0]
        assert t['deserialized'] == expected_deserialization
        self.assertEqual(t['topic'], 'kafkafirst')
        self.assertEqual(t['messages_in_last_hour'], 1)
        last = t['last_messages']
        self.assertEqual(len(last), 1)
        self.assertEqual(last[0]['__partition'], 0)
        self.assertEqual(last[0]['__offset'], 0)
        self.assertEqual(last[0]['__key'], None)
        self.assertEqual(last[0]['__value'], '''{"test": 3}''')
        self.assertEqual(last[0]['__headers'], '')

    @tornado.testing.gen_test
    @patch('tinybird.data_connector.KafkaSettings.PREVIEW_POLL_TIMEOUT_MS', 2000)
    async def test_kafka_preview_all_params_happy_with_headers(self):
        self.produce_message('{"test": 3}', "kafkafirstwithheaders", {"h1": "1", "h2": "42.2"})
        conn = self.create_kafka_connector()
        r = await KafkaUtils.get_kafka_preview(conn,
                                               'test_groupid',
                                               kafka_topics=['kafkafirstwithheaders'])
        assert r.get('error', None) is None
        output = r['preview']
        expected_deserialization = {
            'data': [{'test': 3}],
            'meta': [{'name': 'test', 'type': 'Int16'}],
            'rows': 1,
            'statistics': mock.ANY
        }
        self.assertEqual(len(output), 1)
        t = output[0]
        assert t['deserialized'] == expected_deserialization
        self.assertEqual(t['topic'], 'kafkafirstwithheaders')
        self.assertEqual(t['messages_in_last_hour'], 1)
        last = t['last_messages']
        self.assertEqual(len(last), 1)
        self.assertEqual(last[0]['__partition'], 0)
        self.assertEqual(last[0]['__offset'], 0)
        self.assertEqual(last[0]['__key'], None)
        self.assertEqual(last[0]['__value'], '''{"test": 3}''')
        self.assertEqual(last[0]['__headers'], '{"h1":"1","h2":"42.2"}')

    @tornado.testing.gen_test
    async def test_kafka_preview_topic_notexists(self):
        conn = self.create_kafka_connector()
        r = await KafkaUtils.get_kafka_preview(conn,
                                               'test_groupid',
                                               kafka_topics=['kafka_not_exists123'],
                                               preview_activity=True)
        self.assertEqual(r['error'], 'not_exists')

    @tornado.testing.gen_test
    @patch('tinybird.data_connector.KafkaSettings.PREVIEW_POLL_TIMEOUT_MS', 2000)
    async def test_kafka_preview_connector_id(self):
        self.produce_message("msg2", "kafkasecond")
        conn = self.create_kafka_connector()

        r = await KafkaUtils.get_kafka_preview(data_connector=conn, kafka_group_id='test_groupid', kafka_topics=['kafkasecond'])
        output = r['preview']
        self.assertEqual(len(output), 1)
        t = output[0]
        self.assertEqual(t['topic'], 'kafkasecond')
        self.assertEqual(t['messages_in_last_hour'], 1)
        self.assertEqual(t['committed'], False)
        last = t['last_messages']
        self.assertEqual(len(last), 1)
        self.assertEqual(last[0]['__partition'], 0)
        self.assertEqual(last[0]['__offset'], 0)
        self.assertEqual(last[0]['__key'], None)
        self.assertEqual(last[0]['__value'], "msg2")
        self.assertEqual(last[0]['__headers'], '')

    @tornado.testing.gen_test
    @patch('tinybird.data_connector.KafkaSettings.PREVIEW_POLL_TIMEOUT_MS', 2000)
    async def test_kafka_preview_connector_id_with_headers(self):
        self.produce_message("msg2", "kafkasecondwithheaders", {"h1": "1", "h2": "42.2"})
        conn = self.create_kafka_connector()

        r = await KafkaUtils.get_kafka_preview(data_connector=conn, kafka_group_id='test_groupid',
                                               kafka_topics=['kafkasecondwithheaders'])
        output = r['preview']
        self.assertEqual(len(output), 1)
        t = output[0]
        self.assertEqual(t['topic'], 'kafkasecondwithheaders')
        self.assertEqual(t['messages_in_last_hour'], 1)
        self.assertEqual(t['committed'], False)
        last = t['last_messages']
        self.assertEqual(len(last), 1)
        self.assertEqual(last[0]['__partition'], 0)
        self.assertEqual(last[0]['__offset'], 0)
        self.assertEqual(last[0]['__key'], None)
        self.assertEqual(last[0]['__value'], "msg2")
        self.assertEqual(last[0]['__headers'], '{"h1":"1","h2":"42.2"}')

    @tornado.testing.gen_test
    def test_is_kafka_isolated_for_ws(self):

        user_account = UserAccount.register(f'test_kafka_preview{uuid.uuid4().hex}@mail', 'pass')
        workspace = self.register_workspace(f'test_kafka_preview_ws_{uuid.uuid4().hex}', user_account.id)
        assert KafkaTbUtils._is_isolated(workspace) is False

        workspace_mod = Users.alter_kafka_server_group(workspace, "test_server_group")
        assert KafkaTbUtils._is_isolated(workspace_mod) is True

        assert KafkaTbUtils._get_client(workspace) is None, "Should not be able to get client without server group configured"
        assert KafkaTbUtils._get_client(workspace_mod) is None, "Should not be able to get client without config the server group"
        KafkaServerGroupsConfig.config({"test_server_group": ["localhost:8500"]})
        assert KafkaTbUtils._get_client(workspace_mod) is not None, "Should be able to get client with config the server group and config ok"

    @tornado.testing.gen_test
    @patch('tinybird.kafka_utils.KafkaUtils.get_kafka_preview', return_value={'preview': {}})
    @patch('tinybird.kafka_utils.KafkaUtils.get_kafka_topic_group', return_value={'response': "ok"})
    async def test_kafkatbUtils_with_server_group_should_call_kafka_utils(self, mock_group, mock_preview):
        user_account = UserAccount.register(f'test_kafka_preview{uuid.uuid4().hex}@mail', 'pass')
        workspace = self.register_workspace(f'test_kafka_preview_ws_{uuid.uuid4().hex}', user_account.id)

        conn = data_connector.DataConnector.add_connector(user=workspace, name="name", service='kafka', settings={
            'kafka_bootstrap_servers': 'localhost:9093',
            'kafka_security_protocol': 'plaintext',
            'kafka_sasl_plain_username': '',
            'kafka_sasl_plain_password': '',
        })

        await KafkaTbUtils.get_kafka_preview(workspace, conn, 'test_groupid', 'topic')
        mock_preview.assert_called_once()

        await KafkaTbUtils.get_kafka_topic_group(workspace, conn, 'topic', 'group')
        mock_group.assert_called_once()

    @tornado.testing.gen_test
    @patch('tinybird.kafka_utils.TBAKafkaClient.get_preview', return_value={'preview': {}})
    @patch('tinybird.kafka_utils.TBAKafkaClient.get_kafka_topic_group', return_value={'response': "ok"})
    async def test_kafkatbUtils_with_server_group_should_call_tbakafka_client(self, mock_group, mock_preview):
        user_account = UserAccount.register(f'test_kafka_preview{uuid.uuid4().hex}@mail', 'pass')
        workspace = self.register_workspace(f'test_kafka_preview_ws_{uuid.uuid4().hex}', user_account.id)
        server_group = "test_server_group"
        workspace = Users.alter_kafka_server_group(workspace, server_group)
        KafkaServerGroupsConfig.config({server_group: ["localhost:8500"]})

        conn = data_connector.DataConnector.add_connector(user=workspace, name="name", service='kafka', settings={
            'kafka_bootstrap_servers': 'localhost:9093',
            'kafka_security_protocol': 'plaintext',
            'kafka_sasl_plain_username': '',
            'kafka_sasl_plain_password': '',
        })

        await KafkaTbUtils.get_kafka_preview(workspace, conn, 'test_groupid', 'topic')
        mock_preview.assert_called_once()

        await KafkaTbUtils.get_kafka_topic_group(workspace, conn, 'topic', 'group')
        mock_group.assert_called_once()

    @tornado.testing.gen_test
    async def test_kafka_isolated_get_preview_happy_path(self):
        with patch("tornado.httpclient.AsyncHTTPClient.fetch", new_callable=AsyncMock) as mock:
            mock.return_value = HTTPResponse(HTTPRequest(url="http://localhost:8500"), 200, buffer=BytesIO(b'{"preview": {}}'))
            client = TBAKafkaClient("http://localhost:8500")
            connector = data_connector.DataConnector()
            connector.id = 1
            expected_group_id = "kafka_group_id"
            expected_kafka_topic = "kafka_topic"
            expected_max_records = 10
            expected_preview_activity = True
            expected_earliest_timestamp = True
            result = await client.get_preview(connector,
                                              kafka_group_id=expected_group_id,
                                              kafka_topic=expected_kafka_topic,
                                              max_records=expected_max_records,
                                              preview_activity=expected_preview_activity,
                                              preview_earliest_timestamp=expected_earliest_timestamp,
                                              schema="schema")

            assert result == {"preview": {}}
            _, kwargs = mock.call_args

            parsed_params = parse_qs(kwargs['body'])
            assert connector.id == int(parsed_params['connector_id'][0])
            assert expected_group_id == parsed_params['kafka_group_id'][0]
            assert expected_kafka_topic == parsed_params['kafka_topic'][0]
            assert expected_max_records == int(parsed_params['max_records'][0])
            assert str(expected_preview_activity) == parsed_params['preview_activity'][0]
            assert str(expected_earliest_timestamp) == parsed_params['preview_earliest_timestamp'][0]
            assert "schema" == parsed_params['schema'][0]
            mock.assert_called_once()

    @tornado.testing.gen_test
    async def test_kafka_isolated_get_preview_error(self):
        with patch("tornado.httpclient.AsyncHTTPClient.fetch", new_callable=AsyncMock) as mock:
            mock.return_value = HTTPResponse(HTTPRequest(url="http://localhost:8500"), 500, buffer=BytesIO(b'{"preview": {}}'))
            client = TBAKafkaClient("http://localhost:8500")
            connector = data_connector.DataConnector()
            connector.id = 1
            expected_group_id = "kafka_group_id"
            expected_kafka_topic = "kafka_topic"
            expected_max_records = 10
            expected_preview_activity = True
            expected_earliest_timestamp = True
            result = await client.get_preview(connector,
                                              kafka_group_id=expected_group_id,
                                              kafka_topic=expected_kafka_topic,
                                              max_records=expected_max_records,
                                              preview_activity=expected_preview_activity,
                                              preview_earliest_timestamp=expected_earliest_timestamp,
                                              schema="schema")

            assert result["error"] == "Error connecting to Kafka broker. Contact support@tinybird.co."
            mock.assert_called_once()

    @tornado.testing.gen_test
    async def test_kafka_isolated_get_kafka_topic_group_error_happy_path(self):
        with patch("tornado.httpclient.AsyncHTTPClient.fetch", new_callable=AsyncMock) as mock:
            mock.return_value = HTTPResponse(HTTPRequest(url="http://localhost:8500"), 200, buffer=BytesIO(b'{"preview": {}}'))  # TODO
            client = TBAKafkaClient("http://localhost:8500")
            connector = data_connector.DataConnector()
            connector.id = 1
            expected_group_id = "kafka_group_id"
            expected_kafka_topic = "kafka_topic"
            result = await client.get_kafka_topic_group(connector,
                                                        kafka_topic=expected_kafka_topic,
                                                        kafka_group_id=expected_group_id)

            assert result == {"preview": {}}
            _, kwargs = mock.call_args

            parsed_params = parse_qs(kwargs['body'])
            assert connector.id == int(parsed_params['connector_id'][0])
            assert expected_group_id == parsed_params['kafka_group_id'][0]
            assert expected_kafka_topic == parsed_params['kafka_topic'][0]
            mock.assert_called_once()

    @tornado.testing.gen_test
    async def test_kafka_isolated_get_kafka_topic_group_error(self):
        with patch("tornado.httpclient.AsyncHTTPClient.fetch", new_callable=AsyncMock) as mock:
            mock.return_value = HTTPResponse(HTTPRequest(url="http://localhost:8500"), 500, buffer=BytesIO(b'{"error": {}}'))  # TODO
            client = TBAKafkaClient("http://localhost:8500")
            connector = data_connector.DataConnector()
            connector.id = 1
            expected_group_id = "kafka_group_id"
            expected_kafka_topic = "kafka_topic"
            result = await client.get_kafka_topic_group(connector,
                                                        kafka_topic=expected_kafka_topic,
                                                        kafka_group_id=expected_group_id)

            assert result["error"] == "Error connecting to Kafka broker. Contact support@tinybird.co."
            mock.assert_called_once()


class TestKafkaInvalidParams(BaseTest):
    @tornado.testing.gen_test
    @patch('tinybird.data_connector.KafkaSettings.PREVIEW_POLL_TIMEOUT_MS', 10)
    async def test_kafka_preview_all_params_invalid(self):
        user_account = UserAccount.register(f'test_kafka_preview{uuid.uuid4().hex}@mail', 'pass')
        workspace = self.register_workspace(f'test_kafka_preview_ws_{uuid.uuid4().hex}', user_account.id)

        conn = data_connector.DataConnector.add_connector(user=workspace, name="name", service='kafka', settings={
            'kafka_bootstrap_servers': 'localhost:49999',
            'kafka_security_protocol': 'plaintext',
            'kafka_sasl_plain_username': '',
            'kafka_sasl_plain_password': '',
        })

        output = await KafkaUtils.get_kafka_preview(conn,
                                                    'test_groupid')
        self.assertTrue('error' in output)


class TestGCloudScheduler(BaseTest):
    def test_create_data_connector_for_gcscheduler(self):
        connector_name = 'test_gcloud_connector'
        pipe_name = 'test_glcoud_connector_pipe'
        self.workspace = User.get_by_id(self.WORKSPACE_ID)
        copy_pipe = self.workspace.add_pipe(pipe_name, 'SELECT * FROM test_table')

        connector = data_connector.DataConnector.add_connector(
            user=self.workspace,
            name=connector_name,
            service=data_connector.DataConnectors.GCLOUD_SCHEDULER,
            settings={}
        )

        sink = data_connector.DataSink.add_sink(
            data_connector=connector,
            resource=copy_pipe,
            settings={}
        )

        self.assertEqual(sink.data_connector_id, connector.id)

        sink_by_pipe = data_connector.DataSink.get_by_pipe_id(copy_pipe.id)
        self.assertEqual(sink_by_pipe.id, sink.id)


class TestGCSConnector(BaseTest):
    def test_create_data_connector_for_gcs(self):
        connector_name = 'test_gcs_connector'
        pipe_name = f'{connector_name}_pipe'

        self.workspace = User.get_by_id(self.WORKSPACE_ID)
        export_pipe = self.workspace.add_pipe(pipe_name, 'SELECT * FROM test_table')

        connector = data_connector.DataConnector.add_connector(
            user=self.workspace,
            name=connector_name,
            service=data_connector.DataConnectors.GCLOUD_STORAGE,
            settings={
                'gcs_hmac_access_id': 'gcs_hmac_access_id',
                'gcs_hmac_secret': 'gcs_hmac_secret'
            }
        )

        sink_settings = {
            'bucket_path': 'gcs://tinybird-export',
            'file_template': 'date={date}/company_id={company_id}/export',
            'partition_node': 'partition',
            'format': 'CSV'
        }

        sink = data_connector.DataSink.add_sink(
            data_connector=connector,
            resource=export_pipe,
            settings=sink_settings
        )

        self.assertEqual(sink.data_connector_id, connector.id)

        sink_by_pipe = data_connector.DataSink.get_by_pipe_id(export_pipe.id)
        self.assertEqual(sink_by_pipe.id, sink.id)
        self.assertEqual(sink_by_pipe.settings, sink_settings)

    def test_exception_on_missing_parameters(self):
        connector_name = 'test_gcs_connector'
        self.workspace = User.get_by_id(self.WORKSPACE_ID)

        with self.assertRaises(data_connector.InvalidSettingsException):
            _ = data_connector.DataConnector.add_connector(
                user=self.workspace,
                name=connector_name,
                service=data_connector.DataConnectors.GCLOUD_STORAGE,
                settings={
                    'gcs_hmac_access_id': 'gcs_hmac_access_id'
                }
            )


class TestSnowflakeConnector(BaseTest):
    def test_create_snowflake_data_connector_fails_with_no_settings(self):
        connector_name = 'test_snowflake_connector'
        self.workspace = User.get_by_id(self.WORKSPACE_ID)
        with self.assertRaises(data_connector.InvalidSettingsException):
            _ = data_connector.DataConnector.add_connector(
                user=self.workspace,
                name=connector_name,
                service=data_connector.DataConnectors.SNOWFLAKE,
                settings={}
            )

    def test_create_snowflake_data_connector_succeeds_with_all_settings(self):
        connector_name = 'test_snowflake_connector'
        self.workspace = User.get_by_id(self.WORKSPACE_ID)
        settings = {
            'account': 'sf_account',
            'username': 'sf_username',
            'password': 'sf_password',
            'role': 'sf_role',
            'warehouse': 'sf_warehouse',
            'warehouse_size': 'X-Small',
        }
        connector = data_connector.DataConnector.add_connector(
            user=self.workspace,
            name=connector_name,
            service=data_connector.DataConnectors.SNOWFLAKE,
            settings=settings
        )

        self.assertEqual(connector.settings, settings)

    def test_create_snowflake_data_connector_succeeds_with_mandatory_settings(self):
        connector_name = 'test_snowflake_connector'
        self.workspace = User.get_by_id(self.WORKSPACE_ID)
        settings = {
            'account': 'sf_account',
            'username': 'sf_username',
            'password': 'sf_password',
            'role': 'sf_role',
            'warehouse': 'sf_warehouse',
        }
        connector = data_connector.DataConnector.add_connector(
            user=self.workspace,
            name=connector_name,
            service=data_connector.DataConnectors.SNOWFLAKE,
            settings=settings
        )

        self.assertEqual(connector.settings, settings)

    def test_create_snowflake_data_connector_fails_without_all_mandatory_settings(self):
        connector_name = 'test_snowflake_connector'
        self.workspace = User.get_by_id(self.WORKSPACE_ID)

        def _test(settings):
            with self.assertRaises(data_connector.InvalidSettingsException):
                _ = data_connector.DataConnector.add_connector(
                    user=self.workspace,
                    name=connector_name,
                    service=data_connector.DataConnectors.SNOWFLAKE,
                    settings=settings
                )

        _test({'username': 'sf_username', 'password': 'sf_password'})
        _test({'account': 'sf_account', 'password': 'sf_password'})
        _test({'account': 'sf_account', 'username': 'sf_username'})
        _test({'account': 'sf_account', 'username': 'sf_username', 'password': 'sf_password'})
        _test({'account': 'sf_account', 'username': 'sf_username', 'password': 'sf_password', 'role': 'sf_role'})
        _test({'account': 'sf_account', 'username': 'sf_username', 'password': 'sf_password', 'warehouse': 'warehouse'})
