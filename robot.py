from simulator.onboard import OnboardRobot


class YourRobot(OnboardRobot):
    def __init__(self) -> None:
        super().__init__()


def main():
    robot = YourRobot()
    robot.spin()


if __name__ == '__main__':
    main()