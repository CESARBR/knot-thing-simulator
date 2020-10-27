from pathlib import Path
import pytest
import simulator.simulator_core.thing_parser as thing_parser
import tests.simulator_core.test_defs as defs
import json

ACCEPTABLE_DIFFERENCE = 0.000000000000001

test_file_path = str(Path(__file__).parent.parent)
valid_raw_file = test_file_path + "/test_files/valid_raw_config.json"
invalid_raw_json_id = test_file_path + "/test_files/invalid_raw_config_no_id.json"
invalid_raw_json_no_data = (
    test_file_path + "/test_files/invalid_raw_config_no_data.json"
)

valid_thing_file = test_file_path + "/test_files/valid_thing_config.json"
invalid_thing_file = test_file_path + "/test_files/invalid_thing_no_name_config.json"


def test_create_modbus_server_bank_from_invalid_raw_path_returns_empty():
    server_bank = thing_parser.create_modbus_server_bank_from_raw("Invalid")
    assert server_bank == {}


def test_create_modbus_server_bank_from_invalid_raw_json_no_id_returns_empty():
    server_bank = {}
    with pytest.raises(thing_parser.InvalidServerId):
        server_bank = thing_parser.create_modbus_server_bank_from_raw(
            invalid_raw_json_id
        )
    assert server_bank == {}


def test_create_modbus_server_bank_from_invalid_raw_json_no_data_returns_empty():
    server_bank = {}
    with pytest.raises(thing_parser.InvalidDataModel):
        server_bank = thing_parser.create_modbus_server_bank_from_raw(
            invalid_raw_json_no_data
        )
    assert server_bank == {}


def test_create_modbus_server_bank_from_valid_raw_returns_bank():
    server_bank = thing_parser.create_modbus_server_bank_from_raw(valid_raw_file)
    assert server_bank == defs.expeceted_server_from_raw_bank


def test_create_modbus_thing_bank_from_invalid_thing_data_returns_empty():
    thing_bank = {}
    with pytest.raises(thing_parser.InvalidThingModel):
        thing_bank = thing_parser.create_modbus_thing_bank_from_thing(
            invalid_thing_file
        )
    assert thing_bank == {}


def test_create_modbus_server_bank_from_thing():
    thing_bank = thing_parser.create_modbus_thing_bank_from_thing(valid_thing_file)
    assert thing_bank == defs.expeceted_thing_bank


def test_get_modbus_hex_value_from_signed_int_16():
    signed_values = [-20000, -32768, 32767, -32, 32, 0, 2, 15, 16, 255, 256, 4095, 4096]
    expected_sign_value = [
        ["0xB1E0"],
        ["0x8000"],
        ["0x7FFF"],
        ["0xFFE0"],
        ["0x0020"],
        ["0x0000"],
        ["0x0002"],
        ["0x000F"],
        ["0x0010"],
        ["0x00FF"],
        ["0x0100"],
        ["0x0FFF"],
        ["0x1000"],
    ]

    for i in range(len(signed_values)):
        res_sign = thing_parser.modbus_get_hex_value_from_value(signed_values[i])
        assert res_sign == expected_sign_value[i]


def test_get_modbus_hex_value_from_unsigned_int_16():
    unsigned_values = [1, 32, 32768, 65535, 0]

    expected_unsign_value = [["0x0001"], ["0x0020"], ["0x8000"], ["0xFFFF"], ["0x0000"]]
    for i in range(len(unsigned_values)):
        res = thing_parser.modbus_get_hex_value_from_value(unsigned_values[i])
        assert res == expected_unsign_value[i]


def test_get_modbus_hex_value_from_signed_int_32():
    signed_values = [-2147483648, 2147483647, -2000000000]
    expected_sign_value = [
        ["0x8000", "0x0000"],
        ["0x7FFF", "0xFFFF"],
        ["0x88CA", "0x6C00"],
        ["0x7735", "0x9400"],
    ]

    for i in range(len(signed_values)):
        res_sign = thing_parser.modbus_get_hex_value_from_value(signed_values[i])
        assert res_sign == expected_sign_value[i]


def test_get_modbus_hex_value_from_unsigned_int_32():
    unsigned_values = [4294967295, 4294967293, 2294967295]
    expected_unsign_value = [
        ["0xFFFF", "0xFFFF"],
        ["0xFFFF", "0xFFFD"],
        ["0x88CA", "0x6BFF"],
    ]

    for i in range(len(unsigned_values)):
        res = thing_parser.modbus_get_hex_value_from_value(unsigned_values[i])
        assert res == expected_unsign_value[i]


def test_get_modbus_hex_value_from_signed_int_64():
    signed_values = [-9223372036854775808, 9223372036854775807, 5223372036854775807]
    expected_sign_value = [
        ["0x8000", "0x0000", "0x0000", "0x0000"],
        ["0x7FFF", "0xFFFF", "0xFFFF", "0xFFFF"],
        ["0x487D", "0x2531", "0x626F", "0xFFFF"],
    ]

    for i in range(len(signed_values)):
        res = thing_parser.modbus_get_hex_value_from_value(signed_values[i])
        assert res == expected_sign_value[i]


def test_get_modbus_hex_value_from_unsigned_int_64():
    unsigned_values = [18446744073709551615, 10223372036854775807]
    expected_unsign_value = [
        ["0xFFFF", "0xFFFF", "0xFFFF", "0xFFFF"],
        ["0x8DE0", "0xB6B3", "0xA763", "0xFFFF"],
    ]
    for i in range(len(unsigned_values)):
        res = thing_parser.modbus_get_hex_value_from_value(unsigned_values[i])
        assert res == expected_unsign_value[i]


def test_get_modbus_bin_value_from_int():
    test_values = [0, 8, 12, 50, 32, 256]
    expect_values = [
        [0],
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 1, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1],
    ]
    for i in range(len(test_values)):
        res = thing_parser.modbus_get_bin_value_from_value(test_values[i])
        assert res == expect_values[i]


def test_get_modbus_bin_value_from_int_invalid_int():
    test_values = [-1]
    expect_values = [0]

    res = thing_parser.modbus_get_bin_value_from_value(test_values[0])
    assert res == expect_values
