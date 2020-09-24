from abc import ABC, abstractmethod


class IServerAdapter(ABC):
    def __init__(self):
        self.running = False
        super().__init__()

    @abstractmethod
    def start(self) -> bool:
        """Starts protocol' server adapter interface. """
        pass

    @abstractmethod
    def add_data_server(self, server_id) -> bool:
        """ Adds a new data server related to protocol """
        pass

    @abstractmethod
    def add_data_block(
        self, server_id: int, name, block_type, start_address, length
    ) -> bool:
        """ Adds a new data block to server """
        pass

    @abstractmethod
    def set_data_value(self, server_id, block_name, address, value) -> bool:
        """ Sets a value of a server's data block """
        pass

    @abstractmethod
    def stop(self) -> bool:
        """ Stops server """
        pass
