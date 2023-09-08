import threading
import socket
import json
import math
import time


class RepeatTimer(threading.Timer):
    def __init__(self, interval, function, args=[], kwargs={}):
        super().__init__(interval, function, args, kwargs)
        self.__function = function
        self.__args = args
        self.__kwargs = kwargs

    def run(self):
        while not self.finished.wait(self.interval):
            self.__function(*self.__args, **self.__kwargs)


class Robot():
    def __init__(self) -> None:
        self.__subscriptions = {}
        self.__listenThread = None
        self.__bufferSize = (int)(math.pow(2, 16))

    def spin(self) -> None:
        self.__listenThread = threading.Thread(target=self.__intl_listen)
        self.__listenThread.daemon = True
        self.__listenThread.start()

    def __intl_listen(self):
        while True:
            try:
                print("Connecting to simulator...")
                self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__socket.connect(("localhost", 9092))
            except Exception:
                print("Failed to connect to simulator. Retrying...")
                time.sleep(1)
                continue

            print("Connected to simulator")
            while True:
                data = None
                try:
                    data = self.__socket.recv(self.__bufferSize)
                except ConnectionResetError:
                    print("Connection lost [RST]")
                    break

                if not data:
                    print("Connection lost [EOF]")
                    break

                raw_msg = data.decode()
                packet = None
                try:
                    packet = json.loads(raw_msg)
                except Exception:
                    print("Invalid JSON received: " + raw_msg)
                    continue

                opcode = packet["op"]
                if opcode == "publish":
                    topic = packet["topic"]
                    if topic in self.__subscriptions:
                        for callback in self.__subscriptions[packet["topic"]]:
                            if "msg" in packet:
                                callback(packet["msg"])
                            if "data" in packet:
                                callback(packet["data"])

    def is_subscribed(self, topic: str) -> bool:
        return topic in self.__subscriptions

    def subscribe(self, topic: str, callback: callable) -> None:
        if topic not in self.__subscriptions:
            self.__subscriptions[topic] = []

        print(f"Subscribing to {topic}")
        self.__subscriptions[topic].append(callback)

    def publish(self, topic: str, data: any) -> None:
        packet = {
            "op": "publish",
            "topic": topic,
            "msg": data
        }
        try:
            self.__socket.sendall(json.dumps(packet).encode())
        except Exception:
            # print("Failed to publish message")
            pass

    def create_timer(self, period: float, callback: callable) -> threading.Timer:
        timer = RepeatTimer(period, callback)
        timer.daemon = True
        timer.start()
        return timer

    def destroy_timer(self, timer: threading.Timer) -> None:
        timer.cancel()
        return
