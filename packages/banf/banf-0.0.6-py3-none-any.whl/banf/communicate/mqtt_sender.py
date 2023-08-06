import paho.mqtt.client as paho
from paho import mqtt
import threading
import logging
from queue import Queue
import struct
import time
import re
from utils.preprocessing import ForMeasurement
import pyarrow.vendored.version

"""
1. 다수의 파일
2. 파일에 누적되는 데이터 수집 완료 후 사용자가 직접 Software 버튼 눌러서 데이터 송신
"""


class MQTTtool(threading.Thread):
    def __init__(self) -> None:
        threading.Thread.__init__(self, daemon=True)
        self.q = Queue()
        self.client = None
        self.is_running = False
        self.fm = ForMeasurement()

    def on_connect(self, client, userdata, flags, rc, properties=None) -> None:
        if rc == 0:
            logging.info("Connected with MQTT broker. code : " + str(rc))
        else:
            logging.info("Failed connect with MQTT broker. code : " + str(rc))

    def on_publish(self, client, userdata, mid, properties=None) -> None:
        return
        # logging.info(str(mid) + " sent to MQTT broker.")

    def on_disconnect(self, client, userdata, flags, rc=0) -> None:
        logging.info("Disconnected with MQTT broker. code : " + str(rc))

    def connectBroker(
        self, address: str, port: int, username: str, pw: str
    ) -> paho.Client:
        client = paho.Client(client_id="test_pub", userdata=None, protocol=paho.MQTTv5)
        # client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

        client.on_connect = self.on_connect
        client.on_publish = self.on_publish
        client.on_disconnect = self.on_disconnect

        client.username_pw_set(username, pw)
        client.connect(address, port)

        return client

    def publishData(self, topic: str, msg: str) -> None:
        self.client.publish(topic, msg, 0)

    def disconnectBroker(self) -> None:
        self.client.disconnect()

    def put(self, file_path: str) -> None:
        self.q.put(file_path)

    def startThread(self):
        self.is_running = True
        self.start()

    def stopThread(self):
        self.is_running = False

    def run(self) -> None:
        """
        qos 1, 2로 publish 시 짧은 interval로 여러 msg 전송 불가
        qos 0일 시 client가 on_connect callback 응답받기 전에 publish 실행됨
        qos 0으로 publish하면서 해당 문제 해결을 위해 연결 이후 1초 sleep
        """
        # self.client = self.connectBroker(
        #     "f6bab081112e4de99897d2ceee683056.s1.eu.hivemq.cloud",
        #     8883,
        #     "banfsensors",
        #     "qksvmtpstj!#",
        # )

        self.client = self.connectBroker(
            "ec2-3-142-220-42.us-east-2.compute.amazonaws.com",
            1883,
            "banfsensors",
            "qksvmtpstj!#",
        )

        time.sleep(1)  # for on_connect callback on qos 0

        self.client.loop_start()

        while self.is_running:
            if self.q.qsize() > 0:
                file_path = self.q.get()

                while self.is_running:
                    time.sleep(3)
                    file_size = os.path.getsize(file_path)

                    if cur_file_size - file_size == 0:
                        logging.info("mqtt, " + file_path + " sending...")

                        packet_chunk_list = self.fm.transformToSendPacket(file_path)

                        for packet_chunk in packet_chunk_list:
                            self.publishData("banf/sensors", packet_chunk)
                            # time.sleep(0.01)
                        logging.info(file_path + " send complete!")
                        break
                    else:
                        cur_file_size = file_size
            else:
                time.sleep(1)

        time.sleep(0.5)

        self.client.loop_stop()
        time.sleep(0.5)

        self.disconnectBroker()
