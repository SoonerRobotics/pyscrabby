from simulator.onboard import OnboardRobot


# This is a sample robot that inherits from the OnboardRobot class. It will provide you with functions to move your robot that abstracts away details we will cover later.
# You can use this as a template for your own robot.
class SampleRobot(OnboardRobot):
    # This is the constructor for the SampleRobot class. It is called when you create an instance of the class.
    # In our cases, we will use constructors to initialize variables, create timers, and subscribe to topics.
    def __init__(self) -> None:
        super().__init__()

        # This is an example of how to create a timer. The first argument is the time interval in seconds, and the second argument is the function to call when the timer elapses.
        # In this case, we are creating a timer that calls the _on_timer_elapsed function every second (1.0).
        self.create_timer(1.0, self.__on_timer_elapsed)

        # This is an example of how to subscribe to a topic. The first argument is the topic name, and the second argument is the function to call when a message is received.
        # In this case, we are subscribing to the /onboarding/gps topic and calling the __on_gps_update function when a message is received.
        self.subscribe("/onboarding/gps", self.__on_gps_update)
        self.subscribe("/onboarding/MotorFeedback", self.__on_motor_feedback)

        # This is another possible topic that the simulator will broadcast. We likely won't cover this during onboarding, but if you are interested
        # in how to actually use this camera data, just let me (Dylan) know!
        # self.subscribe("/onboarding/camera/compressed", self.__on_camera_update)

    # This is an example of a function that is called when the timer elapses.
    def __on_timer_elapsed(self):
        # This is an example of how to set the forward and angular velocity of the robot.
        # In robot.py, you will notice these methods do not exist. Typically, you would send publish to a topic to control the robot, but this has been abstracted away for the time being.
        self.setVelocity(1.0, 0.0)

    # This is called every time a message is sent on the /onboarding/gps topic.
    #  - latitude (float): The latitude of the robot
    #  - longitude (float): The longitude of the robot
    def __on_gps_update(self, data):
        print("GPS Update: " +
              str(data["latitude"]) + ", " + str(data["longitude"]))

    # This is called every time a message is sent on the /onboarding/MotorFeedback topic.
    #  - delta_x (float): The change in x position since the last update
    #  - delta_y (float): The change in y position since the last update
    #  - delta_theta (float): The change in theta since the last update
    def __on_motor_feedback(self, data):
        print("Motor Feedback: " + str(data["delta_x"]) + ", " +
              str(data["delta_y"]) + ", " + str(data["delta_theta"]))

# This is the main function that is called when you run the script.


def main():
    # This creates an instance of the SampleRobot class.
    robot = SampleRobot()
    # This starts the robot. We will cover why this function is called "spin" later when we begin to learn about ROS.
    robot.spin()


if __name__ == '__main__':
    main()
