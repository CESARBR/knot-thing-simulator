import sys

import modbus_tk
import modbus_tk.defines as cst
from modbus_tk import modbus_tcp

import simulator.protocol_core
from simulator.protocol_core.iserver_adapter import IServerAdapter
import simulator.definitions as defs


class ModbusTkTcpServerAdapter(IServerAdapter):

    _block_type_map = {
        defs.BLOCK_DIGITAL_RO: cst.DISCRETE_INPUTS,
        defs.BLOCK_DIGITAL_RW: cst.COILS,
        defs.BLOCK_REGULAR_RO: cst.ANALOG_INPUTS,
        defs.BLOCK_REGULAR_RW: cst.HOLDING_REGISTERS,
    }

    def __init__(self, logger):
        self.running = False
        self.tcp_server = None
        self._logger = logger

    def __del__(self):
        if self.running:
            self.tcp_server.stop()
            self.running = False

    def start(self):
        """Starts modbus' server adapter interface. """
        try:
            self.tcp_server = modbus_tcp.TcpServer()
            self.tcp_server.start()
            self.running = True
            return self.running
        except:
            self._logger.error(
                "Some error occurred while \
                creating a new tcp_server"
            )
            self.tcp_server.stop()
            self.running = False
            return self.running

    def add_data_server(self, id):
        """ Adds a new modbus server """
        if self.running:
            try:
                self.tcp_server.add_slave(id)
                self._logger.info("Added modbus server with id = %d ", id)
                return True
            except:
                self._logger.error("Error while adding new server (id =%d)", id)
                return False

        else:
            self._logger.warning("Tcp server not running yet")
            return False

    def add_data_block(self, server_id, name, block_type, start_address, length):
        """ Adds a new block of register to a modbuser server """
        if self.running:
            try:
                self._logger.info(
                    "Adding block for server (%d) - block name (%s) \
                    - start_address (%d) and length (%d).",
                    server_id,
                    name,
                    start_address,
                    length,
                )
                server = self.tcp_server.get_slave(server_id)
                mapped_block = self._block_type_map[block_type]
                if mapped_block == None:
                    return False
                server.add_block(name, mapped_block, start_address, length)
                return True
            except:
                self._logger.error("Error occured while adding new block.")
                return False
        else:
            self._logger.warning("Tcp server not running yet.")
            return False

    def set_data_value(self, server_id, block_name, address, values):
        """ Updates a modbus server register value """
        if self.running:
            try:
                server = self.tcp_server.get_slave(server_id)
                server.set_values(block_name, address, values)
                self._logger.info(
                    "Set data value [%s] to server %d address %d",
                    values,
                    server_id,
                    address,
                )
                return True
            except modbus_tk.modbus.OutOfModbusBlockError as ex:
                self._logger.error(
                    "Some error occurred while trying to add  a value to block: %s", ex,
                )
                return False
        else:
            self._logger.warning("Tcp server not running yet.")
            return False

    def stop(self):
        """Stops the tcp server and closes modbus servers
        connections"""
        if self.running:
            self._logger.info("Tcp server: Stopping...")
            self.tcp_server.stop()
            self.running = False
        else:
            self._logger.warning("Tcp server not running.")
        return True
