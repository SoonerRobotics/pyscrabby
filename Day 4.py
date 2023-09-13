import threading
import time
from simulator.onboard import OnboardRobot
import sys
import signal
import math


MAP_WIDTH = 10
MAP_HEIGHT = 10
MAP_PATH = [
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (1, 4),
    (2, 4),
    (3, 4),
    (4, 4),
    (5, 4),
    (6, 4),
    (6, 5),
    (6, 6),
    (6, 7),
    (6, 8),
    (6, 9)
]
GOAL = (6, 9)
MAP = []


# Fill the map with 1s, from -MAP_WIDTH to MAP_WIDTH, and -MAP_HEIGHT to MAP_HEIGHT
for x in range(-MAP_WIDTH, MAP_WIDTH):
    MAP.append([])
    for y in range(-MAP_HEIGHT, MAP_HEIGHT):
        MAP[x + MAP_WIDTH].append(1)

# Fill the path with 0s
for point in MAP_PATH:
    MAP[point[0]][point[1]] = 0


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path


def get_neighbors(current):
    neighbors = []
    if current[0] > 0:
        neighbors.append((current[0] - 1, current[1]))
    if current[0] < MAP_WIDTH - 1:
        neighbors.append((current[0] + 1, current[1]))
    if current[1] > 0:
        neighbors.append((current[0], current[1] - 1))
    if current[1] < MAP_HEIGHT - 1:
        neighbors.append((current[0], current[1] + 1))
    return neighbors


def get_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def get_path(start, goal):
    closed_set = []
    open_set = [start]
    came_from = {}

    g_score = {}
    f_score = {}

    g_score[start] = 0
    f_score[start] = get_distance(start, goal)

    while len(open_set) > 0:
        current = open_set[0]
        for point in open_set:
            if f_score[point] < f_score[current]:
                current = point

        if current == goal:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        closed_set.append(current)

        for neighbor in get_neighbors(current):
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + \
                get_distance(current, neighbor)

            if neighbor not in open_set:
                open_set.append(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + \
                get_distance(neighbor, goal)

    return None


class SampleRobot(OnboardRobot):
    def __init__(self) -> None:
        super().__init__()

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.subscribe("/onboarding/position", self.__on_position_update)
        self.subscribe("/onboarding/MotorFeedback", self.__on_motor_feedback)
        self.create_timer(0.1, self.__on_timer_called)

    def getAngleDifference(self, to_angle, from_angle):
        delta = to_angle - from_angle
        delta = (delta + math.pi) % (2 * math.pi) - math.pi
        return delta

    def __on_position_update(self, data):
        self.x = data["x"]
        self.y = data["y"]
        pass

    def __on_timer_called(self):
        # Get the current goal
        currentPath = get_path((math.floor(self.x), math.floor(self.y)), GOAL)
        if currentPath is None:
            return
        print(currentPath)
        goal = currentPath[len(currentPath) - 1]

        # Calculate the angle difference between the current goal and the robot's current position
        angle_diff = math.atan2(goal[0] - self.x, goal[1] - self.y)

        # Calculate the error between the current angle and the goal angle
        error = self.getAngleDifference(angle_diff * -1, self.theta) / math.pi

        # Calculate the forward speed based on the error
        forward_speed = 1.0 * (1 - abs(error)) ** 5

        # Calculate the distance between the robot and the current goal point
        distance = math.sqrt((goal[0] - self.x) ** 2 + (goal[1] - self.y) ** 2)
        self.setVelocity(forward_speed, error * 1.65)

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
