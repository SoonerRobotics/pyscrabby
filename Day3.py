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
        self.goals = [(5.0, 6.0), (7.5, 10.0), (10.0, 15.0), (-3.0, 20.0), (-18, 18), (-13, 8)]
        self.goalIndex = 0

        self.subscribe("/onboarding/position", self.__on_position_update)
        self.subscribe("/onboarding/MotorFeedback", self.__on_motor_feedback)
        self.create_timer(0.1, self.__on_timer_called)

    def getAngleDifference(self, to_angle, from_angle):
            delta = to_angle - from_angle
            delta = (delta + math.pi) % (2 * math.pi) - math.pi
            return delta

    def __on_position_update(self, data):
        # print("Position Update: " + str(data["x"]) + ", " + str(data["y"]))
        self.x = data["x"]
        self.y = data["y"]
        pass

    def __on_timer_called(self):
        # Get the current goal
        goal = self.goals[self.goalIndex]

        # Calculate the angle difference between the current goal and the robot's current position
        angle_diff = math.atan2(goal[0] - self.x, goal[1] - self.y)

        # Calculate the error between the current angle and the goal angle
        error = self.getAngleDifference(angle_diff * -1, self.theta) / math.pi

        # Calculate the forward speed based on the error
        forward_speed = 1.0 * (1 - abs(error)) ** 5

        # Calculate the distance between the robot and the current goal point
        distance = math.sqrt((goal[0] - self.x) ** 2 + (goal[1] - self.y) ** 2)

        print("\033c")
        print("Current Goal: " + str(self.goals[self.goalIndex]))
        print("Position: " + str(self.x) + ", " + str(self.y) + ", " + str(self.theta) + " | " + str(math.degrees(self.theta)))
        print("Angle Difference: " + str(angle_diff) + " | " + str(math.degrees(angle_diff)))
        print("Error: " + str(error))
        print("Distance: " + str(distance))
        if distance > 1.5:
            # Set the velocity of the robot
            self.setVelocity(forward_speed, error * 1.65)
        else:
            # Increase the goal index, if its greater than the length of the goals, reset it to 0
            self.goalIndex = self.goalIndex + 1
            if self.goalIndex == len(self.goals):
                self.goalIndex = 0

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
