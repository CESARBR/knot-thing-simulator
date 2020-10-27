from simulator import definitions

expeceted_server_from_raw_bank = {
    "id": 1,
    "register_data": {
        "data_blocks": [
            {"address": 0, "value": ["0xEA60"]},
            {"address": 10, "value": ["0x6C00", "0x88CA"]},
            {"address": 20, "value": ["0x2800", "0xEE6B"]},
            {"address": 30, "value": ["0x0000", "0xFB12", "0x03D3", "0xF0BC"]},
            {"address": 40, "value": ["0x0000", "0x314C", "0xD9B8", "0x98A7"]},
        ],
        "length": 44,
        "start_address": 0,
    },
    "digital_data": {
        "data_blocks": [
            {"address": 0, "value": [1]},
            {"address": 16, "value": [0, 1, 0, 1, 1, 1, 1, 1]},
        ],
        "length": 24,
        "start_address": 0,
    },
}

expeceted_thing_bank = {
    "BM20": {
        "id": 1,
        "register_data": {
            "data_blocks": [
                {
                    "address": 0,
                    "value": ["0x0028"],
                    "sensor_model": {
                        "name": "pressure",
                        "mean": 42,
                        "standard_deviation": 2.0,
                        "sampling_rate": 60,
                    },
                }
            ],
            "length": 1,
            "start_address": 0,
        },
        "digital_data": {
            "data_blocks": [
                {
                    "address": 0,
                    "value": [1, 0, 0, 1],
                    "sensor_model": {
                        "name": "digital_in",
                        "mean": 0,
                        "standard_deviation": 0.0,
                        "sampling_rate": "15",
                    },
                }
            ],
            "length": 4,
            "start_address": 0,
        },
    }
}
