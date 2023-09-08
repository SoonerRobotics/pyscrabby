import threading
import time
from simulator.onboard import OnboardRobot
import sys
import signal
import math


class SampleRobot(OnboardRobot):
    def __init__(self) -> None:
        super().__init__()

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.goals = [(5, 6), (10, 15), (-3, 20), (-18, 18), (-13, 8)]
        self.goalIndex = 0

        self.create_timer(1.0, self.__on_timer_elapsed)

        self.subscribe("/onboarding/position", self.__on_position_update)
        self.subscribe("/onboarding/MotorFeedback", self.__on_motor_feedback)

    def getAngleDifference(self, to_angle, from_angle):
            delta = to_angle - from_angle
            delta = (delta + math.pi) % (2 * math.pi) - math.pi
            return delta

    def __on_timer_elapsed(self):
        print("Position: " + str(self.x) + ", " + str(self.y) + ", " + str(self.theta))
        goal = self.goals[self.goalIndex]
        angle_diff = math.atan2(goal[1] - self.y, goal[0] - self.x)
        error = self.getAngleDifference(angle_diff, self.theta)
        forward_speed = 1.0 * (1 - abs(error)) ** 5
        distance = math.sqrt((goal[0] - self.x) ** 2 + (goal[1] - self.y) ** 2)
        if distance > 0.25:
            self.setVelocity(forward_speed, error * -2)
        else:
            self.goalIndex = self.goalIndex + 1
            if self.goalIndex == len(self.goals):
                self.goalIndex = 0

    def __on_position_update(self, data):
        print("Position Update: " + str(data["x"]) + ", " + str(data["y"]))
        self.x = data["x"]
        self.y = data["y"]
        pass

    def __on_motor_feedback(self, data):
        self.theta = self.theta + data["delta_theta"]

# This is the main function that is called when you run the script.


def main():
    # This creates an instance of the SampleRobot class.
    robot = SampleRobot()
    # This starts the robot. We will cover why this function is called "spin" later when we begin to learn about ROS.
    robot.spin()


def singal_handler(sig, frame):
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, singal_handler)
    main()

    while threading.active_count() > 0:
        time.sleep(1)
