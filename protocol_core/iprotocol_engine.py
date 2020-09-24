from abc import ABC, abstractmethod


class IProtocolEngine:
    _adapter = None
    _server_data_map = []

    def __init__(self, adapter):
        self._adapter = adapter
        pass

    @abstractmethod
    def load_things(self, things) -> bool:
        """Carrega uma lista de things e cria os blocos no
        servidor de modbus"""
        pass

    @abstractmethod
    def set_things_values(self, things_values) -> bool:
        """ Seta os valores das things """
        pass

    @abstractmethod
    def _update(self) -> bool:
        """Atualiza os valores dos registradores do servidor modbus
        com os valores atuais das things periodicamente"""
        pass

    @abstractmethod
    def set_update_timer(self, timeout):
        """Seta os valor de timeout para atualizar os registers
        do modbus"""
        pass
