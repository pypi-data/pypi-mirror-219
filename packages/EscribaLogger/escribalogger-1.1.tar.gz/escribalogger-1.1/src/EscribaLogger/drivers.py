import logging
import os
from datetime import datetime
from typing import Optional, TypedDict

from rich.highlighter import Highlighter
from rich.logging import RichHandler
from rich.text import Text


class DriverOption(TypedDict):
    file_location: Optional[str]


def driver_file(driver_option: DriverOption = None):
    if not driver_option:
        driver_option = {"file_location": "logs"}

    formatter_string = "[%(asctime)s] "
    formatter_string += "%(name)s.%(levelname)s"
    formatter_string += " - %(message)s"
    formatter_string += "%(extra_context)s"

    formatter = logging.Formatter(formatter_string)
    # formatter.default_time_format = '%Y-%m-%d %H:%M:%s'

    log_file_name = datetime.now().strftime("%Y-%m-%d.log")
    log_file_location = driver_option.get("file_location", "logs")

    log_file_path = os.path.join(log_file_location, log_file_name)

    stream = logging.FileHandler(log_file_path)
    stream.setFormatter(formatter)
    return stream


def driver_stdout(driver_option: DriverOption = None):
    class LogNameHighlighter(Highlighter):
        def highlight(self, text: Text) -> None:
            text.highlight_regex(r"^\w+ - ", style="black italic")

    rich_handler = RichHandler(
        highlighter=LogNameHighlighter(),
        level=logging.DEBUG,
        omit_repeated_times=False,
        tracebacks_show_locals=True,
        tracebacks_extra_lines=True,
        tracebacks_word_wrap=True,
        rich_tracebacks=True,
    )

    formatter_string = "%(name)s - %(message)s"

    formatter = logging.Formatter(formatter_string)
    rich_handler.setFormatter(formatter)

    return rich_handler
