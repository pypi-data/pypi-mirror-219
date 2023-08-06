from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import logging
from utils.etc import pattern
from utils.send_receive import mqtt_sender, s3_sender, prometheus_sender
from queue import Queue
import time
import os


# 파일 생성 이벤트 발생 시 실행할 내용
class MyEventHandler(FileSystemEventHandler):
    def __init__(
        self,
        mqtt_tool: mqtt_sender.MQTTtool,
        s3_tool: s3_sender.S3tool,
        p8s_tool: prometheus_sender.PrometheusTool,
    ) -> None:
        self.mqtt_tool = mqtt_tool
        self.s3_tool = s3_tool
        self.p8s_tool = p8s_tool
        self.current_file = []
        self.max_tire_num = 4

    def on_created(self, event) -> None:
        # TODO: process when a file created in the selected directory
        if (
            event.event_type == "created"
            and event.src_path.split("\\")[-1] not in self.current_file
            and event.is_directory == False
        ):
            self.current_file.append(event.src_path.split("\\")[-1])
            if len(self.current_file) == self.max_tire_num:
                self.current_file = []
            logging.info("{0} Created.".format(event.src_path.split("\\")[-1]))
            time.sleep(0.5)
            file_abs_path = event.src_path

            self.mqtt_tool.put(file_abs_path)
            self.s3_tool.put(file_abs_path)
            self.p8s_tool.put(file_abs_path)


# 파일 생성 감지
class FileObserver(pattern.Singleton):
    def __init__(self) -> None:
        self.observer = None
        self.mqtt_tool = None
        self.s3_tool = None
        self.p8s_tool = None

    def setObserver(self, path: str) -> None:
        self.observer = Observer()
        self.mqtt_tool = mqtt_sender.MQTTtool()
        self.s3_tool = s3_sender.S3tool()
        self.p8s_tool = prometheus_sender.PrometheusTool()
        event_handler = MyEventHandler(self.mqtt_tool, self.s3_tool, self.p8s_tool)
        self.observer.schedule(event_handler, path, recursive=True)

    def streamingOn(self) -> None:
        self.observer.start()
        # self.mqtt_tool.startThread()
        self.s3_tool.startThread()
        self.p8s_tool.startThread()

    # Streaming Off + Send Data
    def streamingOff(self) -> None:
        self.observer.stop()
        # self.mqtt_tool.stopThread()
        self.s3_tool.stopThread()
        self.p8s_tool.stopThread()
