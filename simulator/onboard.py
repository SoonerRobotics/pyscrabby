from simulator.robot import Robot


class OnboardRobot(Robot):
    def __init__(self) -> None:
        super().__init__()

    def setVelocity(self, forward_velocity: float, angular_velocity: float) -> None:
        self.__intl_update_velocity(forward_velocity, angular_velocity)

    def __intl_update_velocity(self, forward_velocity: float, angular_velocity: float) -> None:
        self.publish("/onboarding/MotorInput", {
            "forward_velocity": forward_velocity,
            "angular_velocity": angular_velocity
        })