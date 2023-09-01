from simulator.robot import Robot

from .types import GPS, MotorFeedback, MotorInput

class WeebWagon(Robot):
    def __init__(self) -> None:
        super().__init__()

        self.subscribe("/autonav/gps", self._gps_callback)
        self.subscribe("/autonav/MotorFeedback", self._feedback_callback)
        self.motorTimer = self.create_timer(0.1, self._timer_callback)

    def _timer_callback(self) -> None:
        self._set_motors(0, 0.5)

    def _gps_callback(self, msg) -> None:
        gps = GPS(msg)
        print("GPS: {}, {}".format(gps.latitude, gps.longitude))

    def _feedback_callback(self, msg) -> None:
        feedback = MotorFeedback(msg)
        print("Feedback: {}, {}, {}".format(feedback.delta_x, feedback.delta_y, feedback.delta_theta))

    def _set_motors(self, angular_velocity: float, forward_velocity: float) -> None:
        self.publish("/autonav/MotorInput", MotorInput(angular_velocity, forward_velocity).__dict__)