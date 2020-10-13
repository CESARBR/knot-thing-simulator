from abc import ABC, abstractmethod


class IProtocolEngine:
    _adapter = None
    _server_data_map = []

    def __init__(self, adapter):
        self._adapter = adapter
        pass

    @abstractmethod
    def load_server(self, data_model: {}) -> bool:
        """ Loads a data model as modbus server """
        pass

    @abstractmethod
    def set_values(self, things_values) -> bool:
        """ Sets a list of values starting at start_address to server_id at
            block_name
        """
        pass
