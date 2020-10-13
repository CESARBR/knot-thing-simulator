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
from simulator.simulator_core.simulator_engine import SimulatorEngine


def exit_simulator(signal, frame):
    print("SIGINT received, closing simulator")
    sys.exit(0)


def helper():
    print(" ### KNoT Thing Simulator ###")
    print(" Usage: make run [OPTION]... [FILE]")
    print(" -c,  --config[FILE]   Load a raw modbus data model")
    print(" -t,  --thing[FILE]    Load a thing data model and starts simulation")
    print(" -h,  --help           Output this helper")


def simulate(config_path, logger, raw_mode):
    facade = ProtocolFacade()
    sim_engine = SimulatorEngine(facade.get_engine(), logger)
    ret = False
    if raw_mode:
        ret = sim_engine.load_raw_model(config_path)
        return ret
    else:
        ret = sim_engine.load_thing_model(config_path)
        if ret:
            sim_engine.start_simulation()
            return True
        else:
            return False


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

    config_path = "config/thing_config.json"
    opts, args = getopt.getopt(argv, "hc:t:", ["config=", "thing="])
    raw_mode = True
    for opt, arg in opts:
        if opt == "-h":
            helper()
            sys.exit()
        elif opt in ("-c", "--config"):
            logger.info("Simulation configured to Raw")
            config_path = arg
            raw_mode = True
        elif opt in ("-t", "--thing"):
            logger.info("Simulation configured to Thing")
            config_path = arg
            raw_mode = False
    success = simulate(config_path, logger, raw_mode)
    if not success:
        logger.error("Error while simulating...")
        sys.exit(1)
    while True:
        try:
            cmd = sys.stdin.readline()
            args = cmd.split(" ")

            if cmd.find("quit") == 0:
                sys.stdout.write("bye-bye\r\n")
                break
        except KeyboardInterrupt:
            logger.warning("SIGINT received, closing simulator")
            sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_simulator)
    main(sys.argv[1:])
