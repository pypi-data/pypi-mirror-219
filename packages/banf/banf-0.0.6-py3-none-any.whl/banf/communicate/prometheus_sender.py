import threading
import logging
from queue import Queue
import time
import os
from utils.preprocessing import ForMeasurement
from prometheus_client import start_http_server, Gauge
import pandas as pd
import re


class PrometheusTool(threading.Thread):
    def __init__(self) -> None:
        threading.Thread.__init__(self, daemon=True)
        self.q = Queue()
        self.is_running = False
        self.fm = ForMeasurement()
        self.g = Gauge("clientpc_file_data", "clientpc_file_data", ["TP", "TS", "item"])

    def put(self, file_path: str) -> None:
        self.q.put(file_path)

    def startThread(self):
        self.is_running = True
        self.start()

    def stopThread(self):
        self.is_running = False

    def readFile(self, file_name: str) -> pd.DataFrame:
        fm = ForMeasurement()
        with open(file_name, "rb") as f:
            try:  # catch OSError in case of a one line file
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b"\n":
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            last_line = f.readline().decode()
        return fm.transformTxtToDataFrame(last_line)

    def setGauge(self, g: Gauge, df: pd.DataFrame, tp: int, ts: int) -> None:
        col = [
            "Pressure",
            "P_Temperature",
            "VBAT_MON",
            "Relative_Humidity",
            "Temperature",
        ]
        for i in col:
            g.labels(*[tp, ts, i]).set(df[i])
            print(i, df[i])

    def run(self) -> None:
        start_http_server(8000)

        time.sleep(1)

        while self.is_running:
            if self.q.qsize() > 0:
                file_path = self.q.get()
                tp = int(re.sub("[^0-9]", "", file_path.split("_")[0]))
                ts = int(re.sub("[^0-9]", "", file_path.split("_")[1]))
                cur_file_size = os.path.getsize(file_path)
                time.sleep(0.1)

                while self.is_running:
                    file_size = os.path.getsize(file_path)

                    if cur_file_size - file_size != 0:
                        cur_file_size = file_size
                        logging.info("p8s upload")
                        ll_df = self.readFile(file_path)
                        self.setGauge(self.g, ll_df, tp, ts)
                    else:
                        break

                    time.sleep(3)

            else:
                time.sleep(0.5)
