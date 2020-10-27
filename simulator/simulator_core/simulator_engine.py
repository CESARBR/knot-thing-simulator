from simulator.simulator_core import thing_parser as tp
from simulator import definitions as defs
from simulator.simulator_core.simulation_worker import SimulationWorker


class SimulatorError(Exception):
    pass


class ProtocolEngineInvalid(SimulatorError):
    def __init__(self, msg):
        self.message = msg


def _is_valid_engine(protocol_engine):
    has_loader = defs.LOAD_SERVER in protocol_engine
    has_set = defs.SET_VALUES_TO_SERVER in protocol_engine
    has_stop = defs.STOP_SERVER in protocol_engine

    if not has_loader or not has_set or not has_stop:
        raise ProtocolEngineInvalid("Error, protocol engine is not valid")


class SimulatorEngine:
    def __init__(self, protocol_engine, logger):
        _is_valid_engine(protocol_engine)
        self._protocol_engine_load = protocol_engine[defs.LOAD_SERVER]
        self._protocol_engine_set = protocol_engine[defs.SET_VALUES_TO_SERVER]
        self._protocol_engine_stop = protocol_engine[defs.STOP_SERVER]
        self._logger = logger
        self._has_thing = False
        self._simulation_schedule = {}
        self._scheduler_worker = []
        self._sim_started = False

    def load_raw_model(self, config_path: str) -> bool:
        """ Loads a raw model to protocol server """
        server_bank = {}
        ret = False
        try:
            server_bank = tp.create_modbus_server_bank_from_raw(config_path)
            if server_bank == {}:
                self._logger.warning(
                    "Error while creating server bank from\
                                     path: %s",
                    config_path,
                )
                return False
            ret = self._protocol_engine_load(server_bank)
        except:
            return False
        else:
            return ret

    def load_thing_model(self, config_path: str) -> bool:
        """ Loads a thing model to protocol server """
        ret = False
        try:
            thing_bank = tp.create_modbus_thing_bank_from_thing(config_path)
            if thing_bank == {}:
                self._logger.warning(
                    "Error while creating server bank from\
                                     path: %s",
                    config_path,
                )
                return False
            server_bank = {}
            for thing in thing_bank:
                self._logger.info("Loading thing model with name: %s", thing)
                server_bank = thing_bank[thing]
                self._logger.info("%s server_bank = %s", thing, server_bank)
                # currently support loading only one Thing.
                # TODO: Add support to more than 1 thing
            ret = self._protocol_engine_load(server_bank)
        except:
            return False
        else:
            self._create_simulation_schedule(server_bank)
            self._has_thing = ret
            return ret

    def _create_simulation_schedule(self, server_bank: {}) -> bool:
        self._simulation_schedule.clear()
        server_id = server_bank[defs.ID]
        sensors = (server_bank[defs.REGISTER_DATA])[defs.BLOCKS]
        for sensor in sensors:
            sensor_data = {}
            model = sensor[defs.SENSOR_MODEL]
            sensor_data[defs.ID] = server_id
            sensor_data[defs.ADDRESS] = sensor[defs.ADDRESS]
            sensor_data[defs.SENSOR_MEAN] = model[defs.SENSOR_MEAN]
            sensor_data[defs.SENSOR_STD] = model[defs.SENSOR_STD]
            sampling_rate = model[defs.SAMPLING_RATE]
            has_scheduler = sampling_rate in self._simulation_schedule
            if has_scheduler:
                self._logger.info("Adding simulation data -> %s", sensor_data)
                self._simulation_schedule[sampling_rate].append(sensor_data)
            else:
                scheduler_data = []
                scheduler_data.append(sensor_data)
                self._logger.info("Adding simulation data -> %s", sensor_data)
                self._simulation_schedule[sampling_rate] = scheduler_data
        self._logger.info("CREATE SCHEDULE: %s", self._simulation_schedule)
        return True

    def start_simulation(self):
        """ Starts a simulation model of a thing """
        if self._has_thing:
            for schedule in self._simulation_schedule:
                scheduler = SimulationWorker(
                    self._protocol_engine_set,
                    schedule,
                    self._simulation_schedule[schedule],
                    self._logger,
                )
                self._sim_started = True
                scheduler.start()
                self._scheduler_worker.append(scheduler)
                scheduler.join()
            return True
        return False
