import sys, getopt
import logging
import json
import signal

from protocol_core.modbus.modbus_server_adapter import ModbusTkTcpServerAdapter
from protocol_core.modbus.modbus_engine import ModbusEngine
from protocol_core import defines as defs

from protocol_core.modbus.load_config import ConfigLoader

engine = None


def exit_simulator(signal, frame):
    print("SIGINT received, closing simulator")
    sys.exit(0)


def main(argv):
    config_path = "config/config.json"
    try:
        opts, args = getopt.getopt(argv, "hc:", ["config="])
    except getopt.GetoptError:
        print("Loading default config file: config/config.json")
    for opt, arg in opts:
        if opt == "-h":
            print("main.py -c <config-file>.json")
            sys.exit()
        elif opt in ("-c", "--config"):
            config_path = arg
    loader = ConfigLoader()
    server_data = loader.load_model(config_path)
    logger = logging.getLogger("knot-simulator")
    console_handler = logging.StreamHandler()
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s\
        - %(message)s"
    )
    console_handler.setFormatter(log_format)
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    adapter = ModbusTkTcpServerAdapter(logger)
    engine = ModbusEngine(adapter, logger)
    ret = engine.load_server(server_data)
    while True:
        cmd = sys.stdin.readline()
        args = cmd.split(" ")

        if cmd.find("quit") == 0:
            sys.stdout.write("bye-bye\r\n")
            break


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_simulator)
    main(sys.argv[1:])
