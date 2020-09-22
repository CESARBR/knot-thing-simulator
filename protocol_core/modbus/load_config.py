import json
import sys

from protocol_core import defines as defs


class ConfigLoader:
    def load_model(self, model_path: str):
        server_model = {}
        with open(model_path) as json_file:
            data = json.load(json_file)
            model_id = data[defs.ID]
            registers = self._parse_registers(data[defs.REGISTER_DATA])
            digitals = self._parse_digitals(data[defs.DIGITAL_DATA])
            server_model[defs.ID] = model_id
            server_model[defs.REGISTER_DATA] = registers
            server_model[defs.DIGITAL_DATA] = digitals
            return server_model

    def _parse_registers(self, registers):
        data_block = {}
        data_block[defs.BLOCKS] = []
        block_len = 0
        start_address = sys.maxsize
        end_address = 0
        for reg in registers:
            reg_model = {}
            reg_address = int(reg[defs.ADDRESS])
            values = reg[defs.DATA_VALUE]
            value_len = len(values)
            if reg_address < start_address:
                start_address = reg_address
            if reg_address > end_address:
                end_address = reg_address
                block_len = (end_address - start_address) + value_len
            reg_model[defs.ADDRESS] = reg_address
            reg_model[defs.DATA_VALUE] = values
            data_block[defs.BLOCKS].append(reg_model)
        data_block[defs.BLOCK_LENGTH] = block_len
        data_block[defs.BLOCK_START_ADDRESS] = start_address
        return data_block

    def _parse_digitals(self, digitals):
        data_block = {}
        data_block[defs.BLOCKS] = []
        block_len = 0
        start_address = sys.maxsize
        end_address = 0
        for discrete in digitals:
            discrete_model = {}
            reg_address = int(discrete[defs.ADDRESS])
            values = discrete[defs.DATA_VALUE]
            value_len = len(values)
            if reg_address < start_address:
                start_address = reg_address
            if reg_address > end_address:
                end_address = reg_address
                block_len = (end_address - start_address) + value_len
            discrete_model[defs.ADDRESS] = reg_address
            discrete_model[defs.DATA_VALUE] = values
            data_block[defs.BLOCKS].append(discrete_model)
        data_block[defs.BLOCK_LENGTH] = block_len
        data_block[defs.BLOCK_START_ADDRESS] = start_address
        return data_block
