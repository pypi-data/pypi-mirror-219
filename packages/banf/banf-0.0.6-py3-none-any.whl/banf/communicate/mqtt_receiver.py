import paho.mqtt.client as paho
from paho import mqtt
import struct
from utils.send_receive import db_inserter
import logging


class MQTTtool:
    def __init__(self) -> None:
        self.client = paho.Client(
            client_id="test_sub", userdata=None, protocol=paho.MQTTv5
        )
        self.db_tool = db_inserter.DBtool()
        self.struct_fmt = "<2HB14HI2fi2dbdb2f"

        # self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message

        self.client.username_pw_set("banfsensors", "qksvmtpstj!#")
        self.client.connect("ec2-3-142-220-42.us-east-2.compute.amazonaws.com", 1883)

    def startSubscribe(self) -> None:
        self.db_tool.startThread()

        self.client.subscribe("banf/sensors", qos=0)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            logging.info("connected OK")
        else:
            logging.info("Bad connection Returned code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        logging.info("disconnected with MQTT broker. code :", str(rc))
        self.db_tool.stopThread()

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        logging.info("subscribed: " + str(mid) + " " + str(granted_qos))

    def on_message(self, client, userdata, msg):
        payload_list = [
            list(i) for i in struct.iter_unpack(self.struct_fmt, msg.payload)
        ]
        print(payload_list)
