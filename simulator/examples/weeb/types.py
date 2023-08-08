import json

class GPS(object):
    def __init__(self, data) -> None:
        self.latitude = data["latitude"]
        self.longitude = data["longitude"]

class MotorFeedback():
    def __init__(self, delta_x, delta_y, delta_theta) -> None:
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_theta = delta_theta

    def __init__(self, data: dict) -> None:
        self.delta_x = data["delta_x"]
        self.delta_y = data["delta_y"]
        self.delta_theta = data["delta_theta"]

class MotorInput():
    def __init__(self, angular_velocity: float, forward_velocity: float) -> None:
        self.angular_velocity = angular_velocity
        self.forward_velocity = forward_velocity