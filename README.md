# knot-modbus-simulator

KNoT Modbus Simulator is part of the KNoT project.
It aims to provide an industry protocol simulator by creating a tcp server instance so that KNoT Things can be described and tested by KNoT ecosystem.


Check out our [currently supported protocols](#supported-protocols).

## Pre-requisites

- [python 3.8.2](https://www.python.org/downloads/release/python-382/) (*other versions may work but are not officially supported*)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [venv](https://docs.python.org/3/library/venv.html)


## Setup

In order to use this project it's necessary to install its dependencies and add the pre-commit hooks, to simplify this process a `Makefile` was used. Since not all users may like the idea of using a makefile in a python project, this README was separated in two sections: the first explaining how to build and run the project with the [Makefile](#installation-and-usage-with-the-makefile) and the second [without it](#manual-installation-and-usage).

### Installation and usage with the Makefile

#### Pre-requisites
- [Make](https://www.gnu.org/software/make/).

#### Installation

First, change your current working directory to the project's root directory and bootstrap the project:

```bash
# change current working directory
$ cd <path/to/knot-thing-simulator>

# install project dependencies
$ make bootstrap
```

#### Usage

In order to run the main script simply use the `make run` command.

### Manual installation and usage

#### Installation

First, change your current working directory to the project's root and then setup up a new Python virtual environment:

```bash
# change current working directory
$ cd <path/to/knot-thing-simulator>

# setup a new python virtual environment
$ python -m venv venv
```

Now, activate the newly create virtual so that dependencies are installed there and not to your global Python installation:

```bash
# activate virtual environment
$ source venv/bin/activate
```

Now, install the project's dependencies with the following command:

```bash
# install project's dependencies
$ pip install -r requirements.txt
```

>_*note*_: in order to leave the virtual environment you created for the project, use the `deactivate` command (from anywhere).

Finally, prepare the project's custom pre-commit hooks:

```bash
# copy the custom hook to the .git folder
$ cp hooks/pre-commit .git/hooks/pre-commit

# install the pre-commit hooks
$ pre-commit install
```

#### Usage
From the root dir run:
``` bash
sudo env PYTHONPATH=. python <file>
```

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

## Supported Protocols

- Modbus

## License

All KNoT Simulator files are under LGPL v2.1 license, you can check `COPYING`
file for details.
