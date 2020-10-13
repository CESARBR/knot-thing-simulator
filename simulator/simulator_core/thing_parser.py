import json
import sys

from simulator import definitions as defs


class ThingParserError(Exception):
    pass


class InvalidServerId(ThingParserError):
    def __init__(self, msg):
        self.message = msg


class InvalidDataModel(ThingParserError):
    def __init__(self, msg):
        self.message = msg


class InvalidSensorModel(ThingParserError):
    def __init__(self, msg):
        self.message = msg


class InvalidThingModel(ThingParserError):
    def __init__(self, msg):
        self.message = msg


def create_modbus_server_bank_from_raw(file_path: str) -> {}:
    """ Creates a modbus model from a raw file """
    server_bank = {}
    try:
        with open(file_path) as json_file:
            server_bank = _create_modbus_server_bank_from_raw(json_file)
    except OSError:
        return {}
    return server_bank


def create_modbus_thing_bank_from_thing(file_path: str) -> {}:
    """ Creates a modbus model from a thing file """
    try:
        with open(file_path) as json_file:
            return _create_modbus_thing_bank_from_thing(json_file)
    except OSError:
        return {}
    return {}


def _create_modbus_server_bank_from_raw(json_file: json) -> {}:
    server_bank = {}
    data = json.load(json_file)
    has_id = defs.ID in data

    if not has_id:
        raise InvalidServerId("Invalid server id (empty)")
    model_id = int(data[defs.ID])
    if model_id < 1:
        raise InvalidServerId("Invalid id (id < 1)")

    if not data[defs.REGISTER_DATA] and not data[defs.DIGITAL_DATA]:
        raise InvalidDataModel("Invalid data model (empty)")

    if data[defs.REGISTER_DATA]:
        registers = _parse_registers(data[defs.REGISTER_DATA])
    else:
        registers = {}

    if data[defs.DIGITAL_DATA]:
        digitals = _parse_digitals(data[defs.DIGITAL_DATA])
    else:
        digitals = {}
    server_bank[defs.ID] = model_id
    server_bank[defs.REGISTER_DATA] = registers
    server_bank[defs.DIGITAL_DATA] = digitals
    return server_bank


def _create_modbus_thing_bank_from_thing(json_file: json) -> {}:
    thing_bank = {}
    data = json.load(json_file)
    id_counter = 1

    reg_start_addr = 0
    disc_start_addr = 0
    for thing in data:
        if _is_valid_thing(thing) is False:
            continue

        server_bank = {}
        reg_curr_addr = 0
        disc_curr_addr = 0
        registers = []
        digitals = []
        thing_name = thing[defs.THING]
        sensors = thing[defs.SENSORS]

        for sensor in sensors:
            if not _is_sensor_valid(sensor):
                continue
            reg_model = {}
            name = sensor[defs.SENSOR_NAME]
            if sensor[defs.SENSOR_TYPE] == "int":
                values = modbus_get_hex_value_from_value(
                    int(sensor[defs.SENSOR_LAST_VALUE])
                )
                mean = float(sensor[defs.SENSOR_MEAN])
                std = float(sensor[defs.SENSOR_STD])
                rate = int(sensor[defs.SAMPLING_RATE])
                reg_model = _create_reg_model(
                    reg_curr_addr, values, name, rate, std, mean
                )
                registers.append(reg_model)
                reg_curr_addr += len(values)

            elif sensor[defs.SENSOR_TYPE] == "bool":
                values = modbus_get_bin_value_from_value(
                    int(sensor[defs.SENSOR_LAST_VALUE])
                )
                rate = sensor[defs.SAMPLING_RATE]
                reg_model = _create_reg_model(disc_curr_addr, values, name, rate)
                disc_curr_addr += len(values)
                digitals.append(reg_model)
            else:
                continue
        reg_data_block = _create_data_block(registers, reg_start_addr, reg_curr_addr)
        disc_data_block = _create_data_block(digitals, disc_start_addr, disc_curr_addr)
        server_bank[defs.ID] = id_counter
        id_counter += 1
        server_bank[defs.REGISTER_DATA] = reg_data_block
        server_bank[defs.DIGITAL_DATA] = disc_data_block
        thing_bank[thing_name] = server_bank
    if thing_bank is None or thing_bank == {}:
        raise InvalidThingModel("Invalid thing model (no thing data)")
    return thing_bank


def _parse_registers(registers: []) -> {}:
    data_block = {}
    data_blocks = []
    block_len = 0
    start_address = sys.maxsize
    end_address = 0
    for reg in registers:
        reg_address = int(reg[defs.ADDRESS])
        values = reg[defs.DATA_VALUE]
        value_len = len(values)
        if reg_address < start_address:
            start_address = reg_address
        if reg_address > end_address:
            end_address = reg_address
            block_len = (end_address - start_address) + value_len
        reg_model = _create_reg_model(reg_address, values)
        data_blocks.append(reg_model)
    data_block = _create_data_block(data_blocks, start_address, block_len)
    return data_block


def _create_reg_model(
    address: int,
    values: [],
    name: str = "",
    sample_rate: int = 0,
    std: float = 0.0,
    mean: float = 0.0,
) -> {}:
    reg_model = {}
    sensor_model = {}
    reg_model[defs.ADDRESS] = address
    reg_model[defs.DATA_VALUE] = values

    if name != "":
        sensor_model[defs.SENSOR_NAME] = name
        sensor_model[defs.SENSOR_MEAN] = mean
        sensor_model[defs.SENSOR_STD] = std
        sensor_model[defs.SAMPLING_RATE] = sample_rate
        reg_model[defs.SENSOR_MODEL] = sensor_model

    return reg_model


def _parse_digitals(digitals: []) -> {}:
    data_block = {}
    data_blocks = []
    block_len = 0
    start_address = sys.maxsize
    end_address = 0
    for discrete in digitals:
        reg_address = int(discrete[defs.ADDRESS])
        values = list(map(int, discrete[defs.DATA_VALUE]))
        value_len = len(values)
        if reg_address < start_address:
            start_address = reg_address
        if reg_address > end_address:
            end_address = reg_address
            block_len = (end_address - start_address) + value_len
        discrete_model = _create_reg_model(reg_address, values)
        data_blocks.append(discrete_model)
    data_block = _create_data_block(data_blocks, start_address, block_len)
    return data_block


def _create_data_block(data_blocks: [], start_addr: int, block_len: int) -> {}:
    data_block = {}
    data_block[defs.BLOCKS] = data_blocks
    data_block[defs.BLOCK_LENGTH] = block_len
    data_block[defs.BLOCK_START_ADDRESS] = start_addr
    return data_block


def _is_sensor_valid(sensor: {}) -> bool:
    has_sensor_name = defs.SENSOR_NAME in sensor
    has_sensor_value = defs.SENSOR_LAST_VALUE in sensor
    has_sensor_type = defs.SENSOR_TYPE in sensor
    has_sample_rate = defs.SAMPLING_RATE in sensor
    if (
        not has_sensor_name
        or not has_sensor_value
        or not has_sensor_type
        or not has_sample_rate
    ):
        return False

    if int(sensor[defs.SAMPLING_RATE]) < 0:
        return False

    if sensor[defs.SENSOR_TYPE] == "int":
        has_mean = defs.SENSOR_MEAN in sensor
        has_std = defs.SENSOR_STD in sensor
        if not has_mean or not has_std:
            return False
        if float(sensor[defs.SENSOR_STD]) < 0:
            return False
    elif sensor[defs.SENSOR_TYPE] != "bool":
        return False
    return True


def _is_valid_thing(thing: {}) -> bool:
    has_name = defs.THING in thing
    has_sensors = defs.SENSORS in thing
    if not has_name or not has_sensors:
        return False
    elif has_name:
        if thing[defs.THING] == "":
            return False
    elif has_sensors:
        if not thing[defs.SENSORS]:
            return False
    return True


def modbus_get_bin_value_from_value(value: int):
    """ Gets a binary representation of an int """
    if value < 0:
        return [0]
    str_bin = "{0:b}".format(value)
    bin_list = []
    bin_list[:0] = str_bin
    bin_value = []
    len_bin = len(bin_list)
    for i in range(len_bin - 1, 0, -1):
        bin_value.append(int(bin_list[i]))
    bin_value.append(int(bin_list[0]))
    return bin_value


def modbus_get_hex_value_from_value(value: int):
    """ Gets a hex representation of an int """
    hex_value = 0
    values = []
    if value < 0:
        bit_size = value.bit_length()
        if bit_size < 16:
            bit_size = 16
        elif bit_size > 16 and bit_size < 32:
            bit_size = 32
        elif bit_size > 32:
            bit_size = 64
        hex_value = hex((value + (1 << bit_size)) % (1 << bit_size))
    else:
        hex_value = hex(value)

    hex_len = len(hex_value)
    current_idx = hex_len - 1
    hex_fill = 3
    current_hex = list("0000")
    while current_idx > 1:
        if hex_fill != 0:
            current_hex[hex_fill] = hex_value[current_idx]
            hex_fill -= 1
        else:
            current_hex[hex_fill] = hex_value[current_idx]
            values.insert(0, "0x" + ("".join(current_hex)).upper())
            hex_fill = 3
        current_idx -= 1
    if hex_fill != 3:
        values.insert(0, "0x" + ("".join(current_hex)).upper())
    return values
