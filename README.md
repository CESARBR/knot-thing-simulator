# knot-modbus-simulator

KNoT Modbus Simulator is part of the KNoT project.
It aims to provide an industry protocol simulator by creating a tcp server instance so that KNoT Things can be described and tested by KNoT ecosystem.
At this moment, the supported industrial protocols are:

- Modbus


## Dependencies
Build:
- python3 or higher
- pyserial v3.1
- modbus-tk v1.1.1

## How to install dependencies:

- Install with pip:
sudo pip3 install -r requirements.txt

## Configure the simulator
The simulator provides an easy configuration template (config/config.json).
In order to create a data server model of industrial things you need to follow the config template, where the fields are explained bellow:

- id: Specifies the data-server id to be modeled, id > 0.
- register_data: Represents a non-discrete (non-binary) data-block.
    - Each register_data has the following fields:
        - address: Identifies data inside the data-block related to non-discrete block.
        - value: List of values with little-endian representation in Hexa-decimal.
- digital_data: Represents a discrete (binary) data-block.
    - Each digital_data has the following fields:
        - address: Identifies data inside the data-block related to discrete block.
        - value: List of values with little-endian representation in binary.

## Running the Simulator
- Running the simulator with template config:
sudo python3 main.py

- Running a simulator with a custom config file:
sudo python3 main.py -c <config_file>.json

## License

All KNoT Simulator files are under LGPL v2.1 license, you can check `COPYING`
file for details.