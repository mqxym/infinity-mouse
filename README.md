# infinity-mouse

![infinity mouse](https://mqxym.de/assets/infinity_mouse.jpg)

Python script that moves the mouse in an ∞ pattern after a set inactivity timeout.

## Requirements

- Python 3.9+
- macOS, Windows, or Linux (X11)
- Packages: see `requirements.txt`
- Linux note: on X11 the script uses `python-xlib` + XTEST for low-level mouse events; if this backend is unavailable it exits with a warning

## Installation

### Using Pip

```bash

mkdir infinity-mouse
cd infinity-mouse && python3 -m venv .venv/ && source .venv/bin/activate

pip install infinity-mouse

# Run the script
infinity-mouse # You may need to allow system access permissions for your terminal app

# Press CTRL+C to exit the script
```

### Using Source

```bash

git clone https://github.com/mqxym/infinity-mouse
cd infinity-mouse && python3 -m venv .venv/ && source .venv/bin/activate && pip install -r requirements.txt

# Run the script
python run.py # You may need to allow system access permissions for your terminal app

# Press CTRL+C to exit the script
```

## Options

- Adjust the `INACTIVITY_TIMEOUT_MIN` and `INACTIVITY_TIMEOUT_MAX` values in the script or use CLI parameters:

```bash
# Run the script with min-max timeout in seconds
infinity-mouse 80-120

# Test the script
infinity-mouse --test

# View options
infinity-mouse -h

```

## Project Goals

- Learn automation like mouse movements and processing of inputs and HMIs
- Learn pattern creation with sinus functions for the infinity movement pattern
- Build and test CI/CD workflows
- Cross-platform Python development
