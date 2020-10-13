from simulator.protocol_core.modbus.modbus_server_adapter import (
    ModbusTkTcpServerAdapter,
)
from simulator.protocol_core.iprotocol_engine import IProtocolEngine
import simulator.definitions as defs


class ModbusEngine(IProtocolEngine):
    _adapter = None
    _data_servers_map = {}

    def __init__(self, adapter: ModbusTkTcpServerAdapter, logger):
        self._adapter = adapter
        self._logger = logger
        ret = adapter.start()
        if ret != True:
            raise InterruptedError("Unable to start tcp server")
        self._has_servers = False
        self._logger.info("Tcp server started")

    def load_server(self, data_model: {}) -> bool:
        """ Loads a data model as modbus server """
        server_id = data_model[defs.ID]
        if server_id in self._data_servers_map:
            return False
        ret = self._adapter.add_data_server(server_id)
        if ret is False:
            return False
        register_len = (data_model[defs.REGISTER_DATA])[defs.BLOCK_LENGTH]
        digital_len = (data_model[defs.DIGITAL_DATA])[defs.BLOCK_LENGTH]
        register_start_address = (data_model[defs.REGISTER_DATA])[
            defs.BLOCK_START_ADDRESS
        ]
        digital_start_address = (data_model[defs.DIGITAL_DATA])[
            defs.BLOCK_START_ADDRESS
        ]
        data_server_registers = {
            defs.REGISTER_DATA: (data_model[defs.REGISTER_DATA])[defs.BLOCKS],
            defs.DIGITAL_DATA: (data_model[defs.DIGITAL_DATA])[defs.BLOCKS],
        }

        if digital_len > 0:
            self._adapter.add_data_block(
                server_id,
                defs.DIGITAL_DATA,
                defs.BLOCK_DIGITAL_RO,
                digital_start_address,
                digital_len,
            )
        if register_len > 0:
            self._adapter.add_data_block(
                server_id,
                defs.REGISTER_DATA,
                defs.BLOCK_REGULAR_RW,
                register_start_address,
                register_len,
            )
        self._data_servers_map[server_id] = data_server_registers
        ret = self._load_blocks(server_id, data_server_registers)
        if ret:
            self._logger.info("Server added: %s", self._data_servers_map)
        else:
            self._logger.error("Server not added.")
        self._has_servers = ret
        return ret

    def _load_blocks(self, server_id: int, data_registers: {}) -> bool:
        ret = False
        for register in data_registers[defs.REGISTER_DATA]:
            start_address = register[defs.ADDRESS]
            block_name = defs.REGISTER_DATA
            values = register[defs.DATA_VALUE]
            ret = self._set_register_value(server_id, block_name, start_address, values)
            if ret:
                self._logger.info(
                    "Added register: %s to server %d", register, server_id
                )
            else:
                self._logger.error(
                    "Failed to add register: %s to server %d", register, server_id
                )

        for digital_in in data_registers[defs.DIGITAL_DATA]:
            start_address = digital_in[defs.ADDRESS]
            block_name = defs.DIGITAL_DATA
            values = digital_in[defs.DATA_VALUE]
            ret = self._set_register_value(server_id, block_name, start_address, values)
            if ret:
                self._logger.info(
                    "Added digital reg: %s to server %d", digital_in, server_id
                )
            else:
                self._logger.error(
                    "Failed to add digital reg: %s to server %d", digital_in, server_id
                )
        return ret

    def _set_register_value(
        self, server_id: int, block_name: str, start_address: int, values: []
    ) -> bool:
        ret = False
        offset = 0
        for value in values:
            reg_value = 0
            if block_name == defs.REGISTER_DATA:
                reg_value = int(value, 16)
            elif block_name == defs.DIGITAL_DATA:
                reg_value = int(value)
            ret = self._adapter.set_data_value(
                server_id, block_name, (start_address + offset), reg_value
            )
            offset += 1
        return ret

    def stop(self):
        """ Stops modbus tcp server """
        self._adapter.stop()

    def set_values(
        self, server_id: int, block_name: str, start_address: int, values: []
    ) -> bool:
        """ Sets a list of values starting at start_address to server_id at
            block_name
        """
        ret = False
        if self._has_servers:
            if server_id in self._data_servers_map:
                address_offset = 0
                for hex_value in values:
                    value = 0
                    current_address = start_address + address_offset
                    if block_name == defs.REGISTER_DATA:
                        value = int(hex_value, 16)
                    elif block_name == defs.DIGITAL_DATA:
                        value = int(hex_value)
                    ret = self._adapter.set_data_value(
                        server_id, block_name, current_address, value
                    )
                    if ret:
                        self._logger.info(
                            "Set value %d for server (%d) at address (%d)",
                            value,
                            server_id,
                            current_address,
                        )
                        address_offset += 1
                    else:
                        self._logger.error(
                            "Error setting value for address %d" " (server id %d)",
                            current_address,
                            server_id,
                        )
                        break
            else:
                self._logger.warning("No server with id (%d) is registered", server_id)
        else:
            self._logger.warning("No server was created yet.")
        return ret
