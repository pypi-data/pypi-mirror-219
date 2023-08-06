import unittest
from .businesscentral import BusinessCentral as businesscentral
from unittest.mock import patch, MagicMock
from requests import Response
from pandas import DataFrame


class TestBusinessCentral(unittest.TestCase):
    def setUp(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {"access_token": "mock_access_token"}

        with patch("requests.post", return_value=response_mock):
            response_mock = MagicMock(spec=Response)
            response_mock.status_code = 200
            response_mock.json.return_value = {"value": [{"id": 1234, "name": "test"}]}

            with patch("requests.get", return_value=response_mock):
                self.client_id = ("your_client_id",)
                self.client_secret = ("your_client_secret",)
                self.tenant_id = ("your_tenant_id",)
                self.environment_id = "your_environment_id"
                self.businesscentral_instance = businesscentral(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    tenant_id=self.tenant_id,
                    environment_id=self.environment_id,
                )

    def test_connection_test_success(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200

        with patch("requests.get", return_value=response_mock):
            result = self.businesscentral_instance.test_connection()

        self.assertEqual(result, "Test connection Succeeded!")

    def test_connection_test_failure(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 401

        with patch("requests.get", return_value=response_mock):
            result = self.businesscentral_instance.test_connection()

        self.assertEqual(
            result, "Connection failed. Please check the client credentials."
        )

    def test_get_data(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {"value": [{"id": 1234, "name": "test"}]}
        mock_entity = "some_mock_entity"

        with patch("requests.get", return_value=response_mock):
            result = self.businesscentral_instance.get_data(entity=mock_entity)

        self.assertIsInstance(result, DataFrame)


if __name__ == "__main__":
    unittest.main()
