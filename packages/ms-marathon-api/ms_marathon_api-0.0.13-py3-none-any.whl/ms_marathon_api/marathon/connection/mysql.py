import logging

import mysql.connector

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class MySQLConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = "3306"
        self.connection = None

        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
        except Exception as e:
            logging.error(f"Error al conectarse a la base de datos: {e}")

    def close(self):
        if self.connection is not None:
            self.connection.close()
        else:
            logging.warning("No hay conexión para cerrar.")

    def execute_query(self, query: str):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)

        results = cursor.fetchall()

        return results
