import sys, getopt
import logging
import json
import signal

from simulator.protocol_core.modbus.modbus_server_adapter import (
    ModbusTkTcpServerAdapter,
)
from simulator.protocol_core.modbus.modbus_engine import ModbusEngine
from simulator.protocol_core.protocol_facade import ProtocolFacade
from simulator import definitions as defs


def exit_simulator(signal, frame):
    print("SIGINT received, closing simulator")
    sys.exit(0)


def main(argv):
    logger = logging.getLogger("simulator_engine")
    console_handler = logging.StreamHandler()
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s\
        - %(message)s"
    )
    console_handler.setFormatter(log_format)
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_simulator)
    main(sys.argv[1:])
