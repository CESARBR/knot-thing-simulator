#o que o modbusEngine vai fazer?

# Vai criar o server adapter
# Vai guardar os registers criados
# Vai setar os regs
from .modbus_server_adapter import ModbusTkTcpServerAdapter
from protocol_core.iprotocol_engine import IProtocolEngine
import protocol_core.defines as defs

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
        register_start_address = (data_model[defs.REGISTER_DATA])\
            [defs.BLOCK_START_ADDRESS]
        digital_start_address = (data_model[defs.DIGITAL_DATA])\
            [defs.BLOCK_START_ADDRESS]
        data_server_registers = {
            defs.REGISTER_DATA: (data_model[defs.REGISTER_DATA])[defs.BLOCKS],
            defs.DIGITAL_DATA: (data_model[defs.DIGITAL_DATA])[defs.BLOCKS]
        }

        if digital_len > 0:
            self._adapter.add_data_block(server_id, defs.DIGITAL_DATA,
                defs.BLOCK_DIGITAL_RO, digital_start_address, digital_len)
        if register_len > 0:
            self._adapter.add_data_block(server_id, defs.REGISTER_DATA,
                defs.BLOCK_REGULAR_RW, register_start_address, register_len)
        self._data_servers_map[server_id] = data_server_registers
        self._load_blocks(server_id, data_server_registers)
        self._logger.info("Server added id (%d):", server_id)
        return ret

    def _load_blocks(self, server_id: int, data_registers: {}) -> bool:
        for register in data_registers[defs.REGISTER_DATA]:
            start_address = register[defs.ADDRESS]
            offset = 0
            for value in register[defs.DATA_VALUE]:
                self._adapter.set_data_value(server_id, defs.REGISTER_DATA,
                    (start_address+offset), int(value, 16))
                offset += 1

        for digital_in in data_registers[defs.DIGITAL_DATA]:
            start_address = digital_in[defs.ADDRESS]
            offset = 0
            for value in digital_in[defs.DATA_VALUE]:
                self._adapter.set_data_value(server_id, defs.DIGITAL_DATA,
                    (start_address+offset), int(value))
                offset += 1

    def stop(self):
        self._adapter.stop()
        
    def _update(self) -> bool:
        """ Atualiza os valores dos registradores do servidor modbus 
            com os valores atuais das things periodicamente """
        return False

    def set_update_timer(self, timeout):
        """ Seta os valor de timeout para atualizar os registers
            do modbus """
    
    def _validate_data_item(self, item: dict) -> bool:
        """ Validates if data item has all fields filled correctly """
        return True
            
            



