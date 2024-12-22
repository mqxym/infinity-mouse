import pyautogui
import sys
import random
import time
import math
import Quartz
from screeninfo import get_monitors

INACTIVITY_TIMEOUT_MIN = 70
INACTIVITY_TIMEOUT_MAX = 100

# Function to move the mouse
def move_mouse(x, y):
    mouse_event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), 0)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, mouse_event)

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


def infinity_movement():
    # Screen width and height
    screen_width, screen_height = pyautogui.size()
    radius = 50

    circle_coordinates = infinity_points(radius, radius * 2)

    start_x = screen_width / 2 - radius
    start_y = screen_height / 2 - radius
    try:
        while True:
            delay = random.uniform(INACTIVITY_TIMEOUT_MIN, INACTIVITY_TIMEOUT_MAX)
            last_pos = pyautogui.position()
            start_time = time.monotonic()
            while True:
                current_pos = pyautogui.position()
                if current_pos != last_pos:
                    last_pos = current_pos
                    start_time = time.monotonic()
                elif time.monotonic() - start_time >= delay:
                    break
                time.sleep(0.3)
            for x, y in circle_coordinates:
                move_mouse(int(start_x + x), int(start_y + y))
                time.sleep(0.003)
            print(".", end='', flush=True)

    except KeyboardInterrupt:
        print("\nExit...")


if __name__ == "__main__":
    infinity_movement()