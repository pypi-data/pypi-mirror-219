import logging

from .DPSingleton import DPSingleton
from .drivers import DriverOption, driver_file, driver_stdout
from .process_extra_context import process_extra_context


class Log(metaclass=DPSingleton):
    root_logger: logging.Logger = logging.getLogger("EscribaLogger")
    drivers = {"file": driver_file, "stdout": driver_stdout}

    def __init__(self, log_name: str = None) -> None:
        self.root_logger.name = log_name
        self.root_logger.setLevel(logging.DEBUG)
        self.add_filter("extra_context", None)

    @staticmethod
    def handle_any_exception(exc_type, exc_value, exc_traceback):
        Log.root_logger.setLevel(logging.DEBUG)
        Log.root_logger.exception(
            "Uncaught exception\n",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    @staticmethod
    def log_name() -> str:
        return Log.root_logger.name

    @staticmethod
    def set_logger_name(name: str):
        Log.root_logger.name = name

    @staticmethod
    def add_filter(filter_name: str, value: str):
        def define_filter(record: logging.LogRecord):
            setattr(record, filter_name, value)
            return True

        Log.root_logger.addFilter(define_filter)

    @staticmethod
    def add_driver(
        driver_name: str = "stdout",
        driver_func: callable = None,
        driver_options: DriverOption = None,
    ):
        if driver_func:
            Log.drivers[driver_name] = driver_func
        elif driver_name not in Log.drivers:
            raise Exception("Driver not exists")

        current_handlers_list = list(
            map(
                lambda handler: type(handler).__name__,
                Log.root_logger.handlers,
            )
        )
        stream = Log.drivers[driver_name](driver_options)
        if type(stream).__name__ in current_handlers_list:
            return

        Log.root_logger.addHandler(stream)

    @staticmethod
    def remove_driver(driver_name: str):
        if not driver_name:
            raise ValueError("You must specify a valid driver name!!!")
        if driver_name not in Log.drivers.keys():
            raise ValueError(
                f'Driver "{driver_name}" not found. Available drivers: {str(Log.drivers.keys())}!!!'
            )

        Log.root_logger.handlers = list(
            filter(
                lambda handler: type(handler).__name__
                != type(Log.drivers[driver_name](driver_option={})).__name__,
                Log.root_logger.handlers,
            )
        )
        del Log.drivers[driver_name]

    @staticmethod
    def clear_drivers():
        Log.root_logger.handlers = []

    @staticmethod
    def info(msg: str, extra: dict = None):
        Log.add_filter("extra_context", process_extra_context(extra))
        Log.root_logger.info(msg, extra=extra)

    @staticmethod
    def warning(msg: str, extra: dict = None):
        Log.add_filter("extra_context", process_extra_context(extra))
        Log.root_logger.warning(msg, extra=extra)

    @staticmethod
    def warn(msg: str, extra: dict = None):
        Log.root_logger.warning(msg, extra=extra)

    @staticmethod
    def error(msg: str, extra: dict = None):
        Log.add_filter("extra_context", process_extra_context(extra))
        Log.root_logger.error(msg, extra=extra)

    @staticmethod
    def critical(msg: str, extra: dict = None):
        Log.add_filter("extra_context", process_extra_context(extra))
        Log.root_logger.critical(msg, extra=extra)
