from gc_google_services_api.bigquery import BigQueryManager

from ms_marathon_api.marathon.connection.mysql import MySQLConnection
from ms_marathon_api.marathon.dto.TimeReportingDTO import TimeReportingDTO
from ms_marathon_api.marathon.queries.marathon import (
    SELECT_ALL_TIMEREPORTING_DATA,
)

BIGQUERY_TABLE_SCHEMA = {
    "company": "STRING",
    "employee": "STRING",
    "msemail": "STRING",
    "client": "STRING",
    "clientname": "STRING",
    "project": "STRING",
    "mscode": "STRING",
    "feecode": "STRING",
    "accountingdate": "TIMESTAMP",
    "recorddate": "TIMESTAMP",
    "minutes": "FLOAT",
}


class MarathonTimeReporting:
    def __init__(self, host, user, password, database):
        self.mysql_connection = MySQLConnection(host, user, password, database)

    def get_timereporting_table_data(self):
        data_to_migrate = self.mysql_connection.execute_query(
            query=SELECT_ALL_TIMEREPORTING_DATA
        )

        timereportings = (
            TimeReportingDTO.load_data(record).__dict__
            for record in data_to_migrate
        )

        self.mysql_connection.close()

        return timereportings

    def export_to_bigquery(self, dataset_id, project_name, table_name, data):
        bigquery_manager = BigQueryManager(
            project_id=project_name, dataset_id=dataset_id
        )

        bigquery_manager.create_table_if_not_exists(
            table_id=table_name, schema=BIGQUERY_TABLE_SCHEMA
        )

        bigquery_manager.load_massive_data(
            rows_to_insert=data, table_name=table_name
        )
