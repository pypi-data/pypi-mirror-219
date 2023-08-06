import unittest
from unittest import mock

from ms_marathon_api.marathon.api.timereporting import (
    BIGQUERY_TABLE_SCHEMA,
    MarathonTimeReporting,
)
from ms_marathon_api.marathon.dto.TimeReportingDTO import TimeReportingDTO
from ms_marathon_api.marathon.queries.marathon import (
    SELECT_ALL_TIMEREPORTING_DATA,
)


class MarathonTimeReportingTest(unittest.TestCase):
    def setUp(self):
        self.mock_mysql_connection = mock.Mock()
        self.marathon_time_reporting = MarathonTimeReporting(
            host="localhost",
            user="user",
            password="password",
            database="database",
        )
        self.marathon_time_reporting.mysql_connection = (
            self.mock_mysql_connection
        )

    @mock.patch(
        "ms_marathon_api.marathon.api.timereporting.BigQueryManager",
        new=mock.Mock(),
    )
    def test_get_timereporting_table_data(self):
        mock_data = [
            {
                "company": "ABC",
                "employee": "John",
                "msemail": "john@example.com",
                "client": "XYZ",
                "clientname": "Client 1",
                "project": "Project 1",
                "mscode": "MS123",
                "feecode": "FEE456",
                "accountingdate": "2022-01-01",
                "recorddate": "2022-01-02",
                "minutes": 60.0,
            },
            {
                "company": "ABC",
                "employee": "Jane",
                "msemail": "jane@example.com",
                "client": "XYZ",
                "clientname": "Client 2",
                "project": "Project 2",
                "mscode": "MS456",
                "feecode": "FEE789",
                "accountingdate": "2022-02-01",
                "recorddate": "2022-02-02",
                "minutes": 120.0,
            },
        ]
        self.mock_mysql_connection.execute_query.return_value = mock_data

        expected_result = [
            TimeReportingDTO.load_data(record).__dict__ for record in mock_data
        ]

        result = list(
            self.marathon_time_reporting.get_timereporting_table_data()
        )

        self.assertEqual(result, expected_result)
        self.mock_mysql_connection.execute_query.assert_called_once_with(
            query=SELECT_ALL_TIMEREPORTING_DATA
        )
        self.mock_mysql_connection.close.assert_called_once()

    @mock.patch("ms_marathon_api.marathon.api.timereporting.BigQueryManager")
    def test_export_to_bigquery(self, mock_bigquery_manager):
        mock_dataset_id = "dataset_id"
        mock_project_name = "project_name"
        mock_table_name = "table_name"
        mock_data = [
            {
                "company": "ABC",
                "employee": "John",
                "msemail": "john@example.com",
                "client": "XYZ",
                "clientname": "Client 1",
                "project": "Project 1",
                "mscode": "MS123",
                "feecode": "FEE456",
                "accountingdate": "2022-01-01",
                "recorddate": "2022-01-02",
                "minutes": 60.0,
            },
            {
                "company": "ABC",
                "employee": "Jane",
                "msemail": "jane@example.com",
                "client": "XYZ",
                "clientname": "Client 2",
                "project": "Project 2",
                "mscode": "MS456",
                "feecode": "FEE789",
                "accountingdate": "2022-02-01",
                "recorddate": "2022-02-02",
                "minutes": 120.0,
            },
        ]

        self.marathon_time_reporting.export_to_bigquery(
            dataset_id=mock_dataset_id,
            project_name=mock_project_name,
            table_name=mock_table_name,
            data=mock_data,
        )

        mock_bigquery_manager.assert_called_once_with(
            project_id=mock_project_name, dataset_id=mock_dataset_id
        )

        mock_bigquery_instance = mock_bigquery_manager.return_value
        mock_bigquery_instance.create_table_if_not_exists.assert_called_once_with(  # noqa: E501
            table_id=mock_table_name, schema=BIGQUERY_TABLE_SCHEMA
        )

        mock_bigquery_instance.load_massive_data.assert_called_once_with(
            rows_to_insert=mock_data, table_name=mock_table_name
        )
