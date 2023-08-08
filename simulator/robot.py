import threading
import socket
import json
import math
import time


class Robot():
    def __init__(self) -> None:
        self.subscriptions = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listenThread = None
        self.bufferSize = (int)(math.pow(2, 16))
        self.connected = False

    def spin(self, multi_thread: bool = False) -> None:
        if multi_thread:
            self.listenThread = threading.Thread(target=self.intl_listen)
            self.listenThread.daemon = True
            self.listenThread.start()
            return

        try:
            self.intl_listen()
        except KeyboardInterrupt:
            pass

    def intl_connect(self):
        while True:
            if self.connected:
                break

            try:
                self.socket.connect(("127.0.0.1", 9092))
                self.connected = True
            except ConnectionRefusedError:
                self.connected = False
                time.sleep(1)
                continue

    def intl_listen(self):
        self.intl_connect()
        while True:
            data = None
            try:
                data = self.socket.recv(self.bufferSize)
            except ConnectionResetError:
                self.connected = False
                self.intl_connect()
                continue

            if not data:
                break
            packet = json.loads(data.decode())
            op = packet["op"]
            if op != "publish":
                continue

            if packet["topic"] in self.subscriptions:
                for callback in self.subscriptions[packet["topic"]]:
                    callback(packet["msg"])

    def is_subscribed(self, topic: str) -> bool:
        return topic in self.subscriptions

    def subscribe(self, topic: str, callback: callable) -> None:
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []

        print(f"Subscribing to {topic}")
        self.subscriptions[topic].append(callback)

    def publish(self, topic: str, data: any) -> None:
        packet = {
            "op": "publish",
            "topic": topic,
            "msg": data
        }
        try:
            self.socket.sendall(json.dumps(packet).encode())
        except Exception:
            self.connected = False
            self.intl_connect()
