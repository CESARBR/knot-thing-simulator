from threading import Thread
import time

import simulator.definitions as defs
import simulator.simulator_core.thing_parser as tp
import simulator.simulator_core.randomizer as rd


class SimulationWorker(Thread):
    def __init__(self, protocol_engine: {}, timeout: int, sensors: [], logger):
        Thread.__init__(self)
        self._protocol_engine = protocol_engine
        self._timeout = timeout
        self._sensors_models = sensors
        self._logger = logger

    def run(self):
        """ Starts a working thread to generate random values for a sensor """
        while True:
            for sensor in self._sensors_models:
                new_value = rd.get_random_value_from_normal(
                    sensor[defs.SENSOR_MEAN], sensor[defs.SENSOR_STD]
                )
                hex_value = tp.modbus_get_hex_value_from_value(new_value)
                self._logger.info(
                    "|| int value %d - hex_value = %s", new_value, hex_value
                )
                ret = self._protocol_engine(
                    sensor[defs.ID], defs.REGISTER_DATA, sensor[defs.ADDRESS], hex_value
                )
                if ret:
                    self._logger.info(
                        "|server: %d| Sensor at address %s set to %d units",
                        sensor[defs.ID],
                        sensor[defs.ADDRESS],
                        new_value,
                    )
                else:
                    self._logger.error(
                        "|server: %d| Failed: Sensor at address %s",
                        sensor[defs.ID],
                        sensor[defs.ADDRESS],
                    )
            time.sleep(self._timeout)
