import logging
import unittest
from io import StringIO
from unittest import mock

from ms_marathon_api.marathon.connection.mysql import MySQLConnection


class TestMySQLConnection(unittest.TestCase):
    @mock.patch("mysql.connector.connect")
    def test_connect_successful(self, mock_connect):
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection

        connection = MySQLConnection(
            "localhost", "user", "password", "database"
        )

        self.assertEqual(connection.connection, mock_connection)
        mock_connect.assert_called_once_with(
            host="localhost",
            user="user",
            password="password",
            database="database",
            port="3306",
        )

        self.assertIsNotNone(connection.connection)

    @mock.patch("mysql.connector.connect")
    def test_connect_exception(self, mock_connect):
        mock_connect.side_effect = Exception("Connection error")
        log_output = StringIO()
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            stream=log_output,
        )

        with self.assertLogs(level=logging.ERROR) as logs:
            connection = MySQLConnection(
                "localhost", "user", "password", "database"
            )

        self.assertIsNone(connection.connection)

        log_messages = logs.output

        self.assertIn(
            "Error al conectarse a la base de datos", log_messages[0]
        )

    @mock.patch("mysql.connector.connect")
    def test_close_connection(self, mock_connect):
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection

        connection = MySQLConnection(
            "localhost", "user", "password", "database"
        )

        connection.close()

        mock_connection.close.assert_called_once()

    @mock.patch("mysql.connector.connect")
    def test_execute_query(self, mock_connect):
        mock_connection = mock.Mock()
        mock_connect.return_value = mock_connection

        connection = MySQLConnection(
            "localhost", "user", "password", "database"
        )

        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchall.return_value = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Jane"},
        ]

        results = connection.execute_query("SELECT * FROM users")

        self.assertEqual(
            results, [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]
        )
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users")
        mock_cursor.fetchall.assert_called_once()
