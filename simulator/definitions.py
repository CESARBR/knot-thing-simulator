# Things config keys
from pathlib import Path


def get_project_root_path() -> Path:
    return Path(__file__).parent.parent


# PROTOCOL MODBUS SERVER BLOCKS #
BLOCK_DIGITAL_RO = 0
BLOCK_DIGITAL_RW = 1
BLOCK_REGULAR_RO = 2
BLOCK_REGULAR_RW = 3

# PROTOCOL MODBUS CONFIG DICT TAGS
ADDRESS = "address"
DATA_VALUE = "value"
REGISTER_DATA = "register_data"
DIGITAL_DATA = "digital_data"
BLOCKS = "data_blocks"
ID = "id"
BLOCK_LENGTH = "length"
BLOCK_START_ADDRESS = "start_address"

# PROTOCOL ENGINE DICT METHODS TAGS
LOAD_SERVER = "load_server"
STOP_SERVER = "stop_server"
SET_VALUES_TO_SERVER = "set_values"