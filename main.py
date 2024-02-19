import pyautogui
import sys
import random
import time
import math
import Quartz
from screeninfo import get_monitors

SLEEP_MIN = 45
SLEEP_MAX = 60

def sleep_print (seconds):
    print ("Sleeping for: " + str(seconds) + " seconds...")
    time.sleep(seconds)

# Function to move the mouse
def move_mouse(x, y):
    mouse_event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), 0)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, mouse_event)

def circle_points(radius):
    points = []
    for theta in range(0, 360, 1):  # incrementing the angle in degrees
        radian = math.radians(theta)
        x = int(radius * math.cos(radian)) + radius
        y = int(radius * math.sin(radian)) + radius
        point = (x, y)

        # Add the point if it's not already in the list (to avoid duplicates)
        if point not in points:
            points.append(point)

    return points


def infinity_points(radius, center_distance):
    points = []
    # Calculate the centers of the two circles
    center1_x, center2_x = center_distance // 2, 3 * center_distance // 2
    center_y = radius

    # Upper half of the left circle (right to left)
    for theta in range(0, 181, 1):
        radian = math.radians(theta)
        x = int(radius * math.cos(radian)) + center1_x
        y = int(radius * math.sin(radian)) + center_y
        points.append((x, y))

    
    # Lower half of the left circle (left to right)
    for theta in range(180, 361, 1):
        radian = math.radians(theta)
        x = int(radius * math.cos(radian)) + center1_x
        y = int(radius * math.sin(radian)) + center_y
        points.append((x, y))

    # Upper half of the right circle (left to right)
    for theta in range(180, -1, -1):
        radian = math.radians(theta)
        x = int(radius * math.cos(radian)) + center2_x
        y = int(radius * math.sin(radian)) + center_y
        points.append((x, y))

    # Lower half of the right circle (right to left)
    for theta in range(360, 179, -1):
        radian = math.radians(theta)
        x = int(radius * math.cos(radian)) + center2_x
        y = int(radius * math.sin(radian)) + center_y
        points.append((x, y))

    return points

def random_movement ():
    screen_width, screen_height = pyautogui.size()

    while True:

        # Generate random X and Y coordinates within the screen size
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)

        pyautogui.moveTo(x, y, duration=1)

        sleep_print(random.randint(SLEEP_MIN,SLEEP_MAX))

def circle_movement():
    # Screen width and height
    screen_width, screen_height = pyautogui.size()

    radius = 70

    circle_coordinates = circle_points(radius)

    start_x = screen_width / 2 - radius
    start_y = screen_height / 2 - radius

    while True:

        for x, y in circle_coordinates:
            move_mouse(x + start_x, y + start_y)
            time.sleep(0.003)

        sleep_print(random.randint(SLEEP_MIN,SLEEP_MAX))

def infinity_movement():
    # Screen width and height
    screen_width, screen_height = pyautogui.size()

    radius = 50

    circle_coordinates = infinity_points(radius, radius * 2)

    start_x = screen_width / 2 - radius
    start_y = screen_height / 2 - radius

    while True:

        for x, y in circle_coordinates:
            move_mouse(x + start_x, y + start_y)
            time.sleep(0.003)

        sleep_print(random.randint(SLEEP_MIN,SLEEP_MAX))

def main():
    actions = {1: circle_movement, 2: random_movement, 3: infinity_movement}
    monitors = get_monitors()
    
    if len(sys.argv) > 1:
        try:
            choice = int(sys.argv[1])
            if choice in actions:
                actions[choice]()
            else:
                print("Invalid choice. Please select a valid option (1-3).")
        except ValueError:
            print("Invalid input. Please enter a valid number (1-3) as a command-line parameter.")
    else:
        while True:
            print("Choose an option:")
            print("1. Circle Movement")
            print("2. Random Movement")
            print("3. Infinity Movement")
            print("4. Exit")
            try:
                choice = int(input("Enter the number of your choice: "))
                if choice in actions:
                    actions[choice]()
                elif choice == 4:
                    print("Exiting the program.")
                    exit()
                else:
                    print("Invalid choice. Please select a valid option (1-4).")
            except ValueError:
                print("Invalid input. Please enter a valid number (1-4).")
if __name__ == "__main__":
    main()