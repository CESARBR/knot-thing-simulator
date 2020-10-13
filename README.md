# knot-modbus-simulator

KNoT Modbus Simulator is part of the KNoT project.
It aims to provide an industry protocol simulator by creating a tcp server instance so that KNoT Things can be described and tested by KNoT ecosystem.


Check out our [currently supported protocols](#supported-protocols).

## Pre-requisites

- [python 3.8.2](https://www.python.org/downloads/release/python-382/) (*other versions may work but are not officially supported*)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [venv](https://docs.python.org/3/library/venv.html)


## Setup

In order to use this project it's necessary to install its dependencies and add the pre-commit hooks, to simplify this process a `bash script` was used. Since not all users may like the idea of using a bash script in a python project, this README was separated in two sections: the first explaining how to build and run the project with the [bash script](#installation-and-usage-with-the-bash) and the second [without it](#manual-installation-and-usage).

### Installation and usage with the Bash

In order to run the simulator `bash script` is necessary to give R/W/E permissions (744 or higher).
#### Installation

First, change your current working directory to the project's root directory and bootstrap the project:

```bash
# change current working directory
$ cd <path/to/knot-thing-simulator>

# install project dependencies
$ ./run_simulator.sh -b
```

#### Usage

You can read the helper by running the command `./run_simulator.sh -h`.

In order to run a RAW simulation of a modbus databank from a config file, use:
`./run_simulator.sh -r <path-to-config-file>`

In order to run a Thing simulation from a config file, use:
`./run_simulator.sh -t <path-to-config-file>`

In order to clean installation of dependencies:
`./run_simulator.sh -a`

In order to clean compiled files:
`./run_simulator.sh -c`

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

### Docker Installation and Usage

#### Pre-requisites

To install the **project's Docker installation pre-requisites**, please follow the instructions in the link below:

- [Docker](https://docs.docker.com/get-docker/)

> _**Note**: if you're using a Linux system, please take a look at [Docker's post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/)!_

#### Building and running

Once you have all pre-requisites installed, change your current working directory to the project's root:

```bash
# change current working directory
$ cd <path/to/knot-thing-simulator>
```

##### Development

In order to build the **Docker development image**, use the command below:

```bash
# build docker image from Dockerfile-dev
$ docker build . --file Dockerfile-dev --tag knot-thing-simulator:dev
```

Finally, run the **development** container with the following command:

```bash
# start the container and clean up upon exit.
$ docker run --rm --publish 502:502 --volume `pwd`:/usr/src/app --tty --interactive knot-thing-simulator:dev
```

>**_Note_**: the `--volume` flag binds and mounts `pwd` (your current working directory) to the container's `/usr/src/app` directory. This means that the changes you make outside the container will be reflected inside (and vice-versa). You may use your IDE to make code modifications, additions, deletions and so on, and these changes will be persisted both in and outside the container.

##### Production

In order to build the **Docker production image**, use the command below:

```bash
# build docker image from Dockerfile
$ docker build . --file Dockerfile --tag knot-thing-simulator
```

Finally, run the **production** container with the following command:

```bash
# start the container and clean up upon exit.
$ docker run --rm --publish 502:502 --volume `pwd`:/usr/src/app --tty --interactive knot-thing-simulator
```

## Configure the simulator

# RAW simulation
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

# Thing simulation
The simulator provides an easy configuration template for thing simulation (config/thing_config.json).
In order to create a thing simulation model you need to follow the config template, where the fields are explained bellow:

- thing: A name for the thing to be modeled.
- sensors: A list of sensors which represents the thing.
  - name: Name for the sensor.
  - last_value: Last measured value of this sensor.
  - type: Sensor value type (Int or Bool).
  - mean: Mean value of this sensor.
  - standard_deviation: Standard deviation of this sensor.
  - sampling_rate: Sampling rate to simulate this sensor.

## Supported Protocols

- Modbus

## License

All KNoT Simulator files are under LGPL v2.1 license, you can check `COPYING`
file for details.
