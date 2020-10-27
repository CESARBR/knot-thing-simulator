import logging

from simulator.protocol_core.modbus.modbus_server_adapter import (
    ModbusTkTcpServerAdapter,
)
from simulator.protocol_core.modbus.modbus_engine import ModbusEngine
from simulator import definitions as defs


class ProtocolFacade:
    def __init__(self):
        self._logger = logging.getLogger("simulator_protocol_core")
        console_handler = logging.StreamHandler()
        log_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s\
            - %(message)s"
        )
        console_handler.setFormatter(log_format)
        self._logger.setLevel(logging.INFO)
        self._logger.addHandler(console_handler)
        self._server_adapter = ModbusTkTcpServerAdapter(self._logger)
        self._engine = ModbusEngine(self._server_adapter, self._logger)

    def get_engine(self) -> {}:
        """ Gets a dict with protocol engine methods """
        engine_map = {
            defs.LOAD_SERVER: self._engine.load_server,
            defs.STOP_SERVER: self._engine.stop,
            defs.SET_VALUES_TO_SERVER: self._engine.set_values,
        }
        return engine_map
