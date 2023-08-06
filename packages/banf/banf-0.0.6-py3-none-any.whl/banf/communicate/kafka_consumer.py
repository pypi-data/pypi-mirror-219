from confluent_kafka import Consumer, KafkaError
import struct
from utils.send_receive import db_inserter
import logging
from utils.preprocessing import ForMeasurement


class KAFKAtool:
    def __init__(self) -> None:
        self.c = Consumer(
            {
                "bootstrap.servers": "pkc-ymrq7.us-east-2.aws.confluent.cloud:9092",
                "group.id": "group_1",
                "auto.offset.reset": "earliest",
                "enable.auto.commit": True,
                "security.protocol": "SASL_SSL",
                "sasl.mechanisms": "PLAIN",
                "sasl.username": "XTY3DPT6HLNF4AFA",
                "sasl.password": "qNnKNg+oSlCCIeNhiiutMki7tSMrvWqCyeOM5hasHuV+djt9sczbMb31sNTcshYf",
            }
        )
        self.db_tool = db_inserter.DBtool()
        self.struct_fmt = "<2HB14HI2fI2dbdb2f"
        self.fm = ForMeasurement()

    def startSubscribe(self) -> None:
        self.db_tool.startThread()

        self.c.subscribe(["sensors"])
        while True:
            msg = self.c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"Reached end of partition {msg.partition()}, continuing...")
                else:
                    print(f"Error while polling for messages: {msg.error()}")

            data_list = [
                list(i) for i in struct.iter_unpack(self.struct_fmt, msg.value())
            ]
            self.db_tool.put(self.fm.transformToReceivePacket(data_list))

    def __exit__(self, type, value, trackback):
        self.c.close()
