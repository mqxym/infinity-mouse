import pyautogui
import sys
import random
import time
import math
import Quartz
from screeninfo import get_monitors
import argparse

# Ideas:
# - Set timeout with CLI parameter or env variables
# - Maybe use last active monitor to draw the infinity symbol on

INACTIVITY_TIMEOUT_MIN = 70
INACTIVITY_TIMEOUT_MAX = 100
TEST_MODE = False

def parse_range(range_str):
    """
    Parse and validate the range string in the format 'min-max'.
    
    Args:
        range_str (str): The range string to parse.
    
    Returns:
        tuple: A tuple of two integers (a, b) if valid.
    
    Raises:
        argparse.ArgumentTypeError: If the format is incorrect or constraints are not met.
    """
    try:
        parts = range_str.split('-')
        if len(parts) != 2:
            raise ValueError
        a_str, b_str = parts
        a = int(a_str)
        b = int(b_str)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Range '{range_str}' is invalid. It must be in the format 'min-max' where min and max are integers."
        )
    
    if not (1 <= a < b <= 1199):
        raise argparse.ArgumentTypeError(
            f"Invalid range '{range_str}'. Ensure that 1 <= min < max <= 1199."
        )
    
    return (a, b)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Moves the mouse after a set inactivity timeout."
    )
    
    # Positional argument for the timeout range
    parser.add_argument(
        'range',
        type=parse_range,
        nargs='?',
        default=None,
        help="The timeout range in the format 'min-max' in seconds where 1 <= min < max <= 1199."
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help="Enable test mode."
    )
    
    args = parser.parse_args()

    global INACTIVITY_TIMEOUT_MAX, INACTIVITY_TIMEOUT_MIN, TEST_MODE
    
    if args.range:
        min, max = args.range
        INACTIVITY_TIMEOUT_MAX = max
        INACTIVITY_TIMEOUT_MIN = min
    TEST_MODE = args.test

# Function to move the mouse with Quartz lib
def move_mouse(x, y):
    mouse_event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), 0)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, mouse_event)

def move_coordinates(start_x, start_y, coordinates): 
    for x, y in coordinates:
        move_mouse(int(start_x + x), int(start_y + y))
        time.sleep(0.003)

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
    parse_arguments()

    # Screen width and height
    screen_width, screen_height = pyautogui.size()
    radius = 50

    circle_coordinates = infinity_points(radius, radius * 2)

    start_x = screen_width / 2 - radius
    start_y = screen_height / 2 - radius

    if TEST_MODE:
        print("Started test!")
        move_coordinates(start_x, start_y, circle_coordinates)
        print("Finished...")
        exit(0)

    try:
        print("Started!")
        # Test if movement possible
        move_mouse(screen_width / 2, screen_height / 2)

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
            move_coordinates(start_x, start_y, circle_coordinates)
            print(".", end='', flush=True)

    except KeyboardInterrupt:
        print("\nExit...")


if __name__ == "__main__":
    infinity_movement()