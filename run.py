import pyautogui
import sys
import random
import time
import math
import Quartz
from screeninfo import get_monitors
import argparse

# Ideas:
# - Maybe use last active monitor to draw the infinity symbol on

INACTIVITY_TIMEOUT_MIN = 70
INACTIVITY_TIMEOUT_MAX = 100
TEST_MODE = False
RADIUS = 50

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


# Currently only main monitor supported, algorithm below fails on some cases
def get_active_monitor_middle():
    return tuple(x / 2 for x in pyautogui.size())

    monitors = get_monitors()
    
    if not monitors:
        return tuple(x / 2 for x in pyautogui.size())
    
    mouse_x, mouse_y = pyautogui.position()
    for monitor in monitors:
        mon_x_min = monitor.x
        mon_x_max = monitor.x + monitor.width

        mon_y_min = monitor.y
        mon_y_max = monitor.y + monitor.height
       
        if (mon_x_min <= mouse_x < mon_x_max and
            mon_y_min <= mouse_y < mon_y_max):
            # Return the monitor's width and height (which remain the same in any coordinate space)
            return monitor.width/2+mon_x_min, monitor.height/2
        
    return tuple(x / 2 for x in pyautogui.size())

def get_start_points(middle_x, middle_y):
    return middle_x-RADIUS*2,middle_y-RADIUS

def disable_icon():
    try:
        from AppKit import NSApplication, NSApplicationActivationPolicyAccessory
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
    except Exception as e:
        print("Failed to remove dock icon:", e)

def infinity_movement():
    parse_arguments()
    if sys.platform == "darwin":
        disable_icon()

    # Screen width and height
    active_middle_x, active_middle_y = get_active_monitor_middle()

    movement_coordinates = infinity_points(RADIUS, RADIUS * 2)

    if TEST_MODE:
        print("Started test!")
        start_x , start_y = get_start_points(active_middle_x, active_middle_y)
        move_coordinates(start_x, start_y, movement_coordinates)
        print("Finished...")
        exit(0)

    try:
        print("Started!")
        # Test if movement possible
        move_mouse(active_middle_x, active_middle_y)

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
            
            # reset middle before move
            active_middle_x, active_middle_y = get_active_monitor_middle()
            start_x , start_y = get_start_points(active_middle_x, active_middle_y)

            move_coordinates(start_x, start_y, movement_coordinates)
            print(".", end='', flush=True)

    except KeyboardInterrupt:
        print("\nExit...")


if __name__ == "__main__":
    infinity_movement()