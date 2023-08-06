import psycopg2
import threading
from queue import Queue
import psycopg2
import time
import logging
from datetime import datetime
import numpy as np
import pandas as pd
from utils.preprocessing import ForMeasurement

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class DBtool(threading.Thread):
    def __init__(self) -> None:
        threading.Thread.__init__(self, daemon=True)
        self.q = Queue()
        self.is_running = False

        self.host = "banf-dataserver.cpk0zcc033nb.us-east-2.rds.amazonaws.com"
        self.dbname = "STPS"
        self.user = "insert_user"
        self.password = "dlstjxm!#"
        self.port = 5432
        self.table_name = "sensor_data"

        self.conn = self.connectConfig(
            self.host, self.dbname, self.user, self.password, self.port
        )
        logging.info("connect with Database Server.")
        self.cur = self.conn.cursor()

        self.cols = self.getColumnsName(self.cur, self.table_name)

    def connectConfig(
        self, host: str, dbname: str, user: str, password: str, port: int
    ) -> psycopg2.extensions.connection:
        return psycopg2.connect(
            host=host, dbname=dbname, user=user, password=password, port=port
        )

    def getColumnsName(self, cur: psycopg2.extensions.cursor, table_name: str) -> list:
        cur.execute("SELECT * FROM " + table_name + " LIMIT 0")
        cur.fetchall()

        return ['"' + desc[0] + '"' for desc in cur.description]

    def insertData(
        self,
        conn: psycopg2.extensions.connection,
        cur: psycopg2.extensions.cursor,
        table_name: str,
        df: pd.DataFrame,
    ) -> None:
        data_dict = {}
        cols = df.columns
        values = df.values

        for i in range(len(cols)):
            if i == 22 or i == 24:
                data_dict[str(i)] = [chr(j[i]) for j in values]
            else:
                data_dict[str(i)] = [j[i] for j in values]

        query = (
            "INSERT INTO " + table_name + " (" + ", ".join(self.cols) + ") \nselect "
        )
        for i in range(len(self.cols)):
            query += "\nunnest(%(" + str(i) + ")s), "

        query = query[:-2]

        cur.execute(query, data_dict)
        conn.commit()

        logging.info("store " + str(len(values)) + " data into server.")

    def startThread(self):
        self.is_running = True
        self.start()

    def stopThread(self):
        self.is_running = False

    def __exit__(self, type, value, trackback):
        self.conn.close()

    def put(self, data_list: list) -> None:
        self.q.put(data_list)

    def run(self) -> None:
        while self.is_running:
            if self.q.qsize() > 0:
                self.insertData(self.conn, self.cur, self.table_name, self.q.get())
            else:
                time.sleep(0.5)

        self.conn.close()
