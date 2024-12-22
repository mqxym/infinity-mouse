# infinity-mouse

![infinity mouse](https://mqxym.de/assets/infinity_mouse.jpg)

Python script that moves the mouse after a set inactivity timeout.

## Requirements

- MacOS with Python3.12+
- Packages: see `requirements.txt`

## Installation

```bash

git clone https://github.com/mqxym/infinity-mouse
cd infinity-mouse && python3 -m venv .venv/ && source .venv/bin/activate && pip install -r requirements.txt

# Run the script
python run.py # You may need to allow system access permissions for your terminal app

# Press CTRL+C to exit the script
```

## Options

- Adjust the `INACTIVITY_TIMEOUT_MIN` and `INACTIVITY_TIMEOUT_MAX` values in the script

## Project Goals

- Learn automation like mouse movements and processing of inputs and HMIs
- Learn pattern creation with sinus functions for the infinity movement pattern

## Future Additions

- Linux and Windows support?
- CLI parameter controls?
