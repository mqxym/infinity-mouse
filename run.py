#!/usr/bin/env python3
import sys
import random
import time
import math
import argparse

import pyautogui

# Optional dependency (only used if you re-enable multi-monitor logic)
# from screeninfo import get_monitors

# ----------------------------
# Config
# ----------------------------
INACTIVITY_TIMEOUT_MIN = 70
INACTIVITY_TIMEOUT_MAX = 100
TEST_MODE = False
RADIUS = 50

# ----------------------------
# Arg parsing
# ----------------------------
def parse_range(range_str: str):
    """
    Parse and validate the range string in the format 'min-max'.
    Returns: (min, max) as ints
    """
    try:
        parts = range_str.split("-")
        if len(parts) != 2:
            raise ValueError
        a = int(parts[0])
        b = int(parts[1])
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

    parser.add_argument(
        "range",
        type=parse_range,
        nargs="?",
        default=None,
        help="The timeout range in the format 'min-max' in seconds where 1 <= min < max <= 1199.",
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help="Enable test mode.",
    )

    args = parser.parse_args()

    global INACTIVITY_TIMEOUT_MAX, INACTIVITY_TIMEOUT_MIN, TEST_MODE

    if args.range:
        mn, mx = args.range
        INACTIVITY_TIMEOUT_MIN = mn
        INACTIVITY_TIMEOUT_MAX = mx

    TEST_MODE = args.test


# ----------------------------
# Platform mouse movement
# ----------------------------
_MOVE_BACKEND = None

def _setup_mouse_backend():
    """
    Selects a low-level-ish backend per platform:
      - macOS: Quartz.CGEventCreateMouseEvent + CGEventPost
      - Windows: SendInput (ctypes)
    - Linux: python-xlib + XTEST
    - Other/Unavailable: raise backend-not-found error
    Sets global _MOVE_BACKEND callable: move_mouse(x,y)
    """
    global _MOVE_BACKEND

    if sys.platform == "darwin":
        # macOS Quartz backend
        import Quartz  # type: ignore

        def move_mouse_mac(x, y):
            ev = Quartz.CGEventCreateMouseEvent(
                None, Quartz.kCGEventMouseMoved, (int(x), int(y)), 0
            )
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, ev)

        _MOVE_BACKEND = move_mouse_mac
        return

    if sys.platform == "win32":
        # Windows SendInput backend (supports multi-monitor / negative coords)
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.WinDLL("user32", use_last_error=True)

        # (Optional but helpful) Make process DPI-aware so coordinates match what Windows uses.
        # This avoids "cursor moves to wrong spot" under scaling in many setups.
        try:
            # Per-monitor DPI awareness (Win 8.1+ / 10+)
            shcore = ctypes.WinDLL("shcore", use_last_error=True)
            shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
        except Exception:
            try:
                user32.SetProcessDPIAware()
            except Exception:
                pass
        
        ULONG_PTR = wintypes.WPARAM

        INPUT_MOUSE = 0
        MOUSEEVENTF_MOVE = 0x0001
        MOUSEEVENTF_ABSOLUTE = 0x8000
        MOUSEEVENTF_VIRTUALDESK = 0x4000

        SM_XVIRTUALSCREEN = 76
        SM_YVIRTUALSCREEN = 77
        SM_CXVIRTUALSCREEN = 78
        SM_CYVIRTUALSCREEN = 79

        class MOUSEINPUT(ctypes.Structure):
            _fields_ = [
                ("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ULONG_PTR),
            ]

        class INPUT(ctypes.Structure):
            _fields_ = [("type", wintypes.DWORD), ("mi", MOUSEINPUT)]

        def _get_virtual_screen_rect():
            vx = user32.GetSystemMetrics(SM_XVIRTUALSCREEN)
            vy = user32.GetSystemMetrics(SM_YVIRTUALSCREEN)
            vw = user32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
            vh = user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)
            return vx, vy, vw, vh

        def move_mouse_win(x, y):
            vx, vy, vw, vh = _get_virtual_screen_rect()

            # Normalize to 0..65535 across *virtual desktop* (inclusive)
            nx = int((int(x) - vx) * 65535 / (vw - 1)) if vw > 1 else 0
            ny = int((int(y) - vy) * 65535 / (vh - 1)) if vh > 1 else 0

            inp = INPUT(
                type=INPUT_MOUSE,
                mi=MOUSEINPUT(
                    dx=nx,
                    dy=ny,
                    mouseData=0,
                    dwFlags=MOUSEEVENTF_MOVE
                    | MOUSEEVENTF_ABSOLUTE
                    | MOUSEEVENTF_VIRTUALDESK,
                    time=0,
                    dwExtraInfo=0,
                ),
            )

            n = user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))
            if n != 1:
                raise ctypes.WinError(ctypes.get_last_error())

        _MOVE_BACKEND = move_mouse_win
        return

    if sys.platform.startswith("linux"):
        # Prefer python-xlib + XTEST on Linux for low-level event injection on X11.
        try:
            from Xlib import display as xdisplay  # type: ignore
            from Xlib.ext import xtest  # type: ignore

            disp = xdisplay.Display()
            root = disp.screen().root

            def move_mouse_linux_xlib(x, y):
                root.warp_pointer(int(x), int(y))
                xtest.fake_input(disp, 6, 0, x=int(x), y=int(y))
                disp.sync()

            _MOVE_BACKEND = move_mouse_linux_xlib
            return
        except Exception:
            pass

    message = (
        "No compatible mouse backend found. "
        "On Linux/X11 install python-xlib; "
        "on macOS ensure Quartz is available; on Windows SendInput is built-in."
    )
    print(f"Warning: {message}", file=sys.stderr)
    raise RuntimeError(message)


def move_mouse(x, y):
    if _MOVE_BACKEND is None:
        _setup_mouse_backend()
    _MOVE_BACKEND(x, y)


# ----------------------------
# Movement path logic
# ----------------------------
def move_coordinates(start_x, start_y, coordinates):
    for x, y in coordinates:
        move_mouse(int(start_x + x), int(start_y + y))
        time.sleep(0.003)


def infinity_points(radius, center_distance):
    points = []
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


# ----------------------------
# Monitor / positioning helpers
# ----------------------------
def get_active_monitor_middle():
    w, h = pyautogui.size()
    return (w / 2, h / 2)


def get_start_points(middle_x, middle_y):
    return middle_x - RADIUS * 2, middle_y - RADIUS


def disable_icon_macos():
    try:
        from AppKit import NSApplication, NSApplicationActivationPolicyAccessory  # type: ignore

        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
    except Exception as e:
        print("Failed to remove dock icon:", e)


# ----------------------------
# Main loop
# ----------------------------
def infinity_movement():
    parse_arguments()

    if sys.platform == "darwin":
        disable_icon_macos()

    # init backend once
    _setup_mouse_backend()

    active_middle_x, active_middle_y = get_active_monitor_middle()
    movement_coordinates = infinity_points(RADIUS, RADIUS * 2)

    if TEST_MODE:
        print("Started test!")
        start_x, start_y = get_start_points(active_middle_x, active_middle_y)
        move_coordinates(start_x, start_y, movement_coordinates)
        print("Finished...")
        sys.exit(0)

    try:
        print("Started!")

        # Test if movement possible (permissions etc.)
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
            start_x, start_y = get_start_points(active_middle_x, active_middle_y)

            move_coordinates(start_x, start_y, movement_coordinates)
            print(".", end="", flush=True)

    except KeyboardInterrupt:
        print("\nExit...")


if __name__ == "__main__":
    infinity_movement()
