import sys

from loguru import logger
import os.path

__loge_msg_format = "[{time:HH:mm:ss}] {message}"

__exception_log_path = os.path.join("logs", "exception", "exception_{time:YYYY-MM-DD}.log")
__connection_log_path = os.path.join("logs", "connection", "connection_{time:YYYY-MM-DD}.log")
__money_log_path = os.path.join("logs", "money", "money_{time:YYYY-MM-DD}.log")
__item_log_path = os.path.join("logs", "item", "item_{time:YYYY-MM-DD}.log")
__system_log_path = os.path.join("logs", "system", "system_{time:YYYY-MM-DD}.log")
__console_log_path = os.path.join("logs", "console", "console_{time:YYYY-MM-DD}.log")
__command_log_path = os.path.join("logs", "command", "command_{time:YYYY-MM-DD}.log")


def __make_filter(name):
    def filter(record):
        return record["extra"].get("name") == name

    return filter


logger.remove()

logger.add(__system_log_path, level="DEBUG", format=__loge_msg_format,
           compression="tar.gz", rotation="1 days", filter=__make_filter("system"))

logger.add(__exception_log_path, level="ERROR", format=__loge_msg_format,
           backtrace=True, diagnose=True,
           compression="tar.gz", rotation="1 days", filter=__make_filter("exception"))

logger.add(__connection_log_path, level="INFO", format=__loge_msg_format,
           compression="tar.gz", rotation="1 days", filter=__make_filter("connection"))

logger.add(__money_log_path, level="INFO", format=__loge_msg_format,
           compression="tar.gz", rotation="1 days", filter=__make_filter("money"))

logger.add(__item_log_path, level="INFO", format=__loge_msg_format,
           compression="tar.gz", rotation="1 days", filter=__make_filter("item"))

logger.add(__command_log_path, level="INFO", format=__loge_msg_format,
           compression="tar.gz", rotation="1 days", filter=__make_filter("command"))

logger.add(sys.stdout, level="DEBUG", format="{time} | {level} | {message}", backtrace=True, diagnose=True,
           filter=__make_filter("debugger"))

logger.add(__console_log_path, level="DEBUG", format="{time} | {level} | {message}",
           compression="tar.gz", rotation="1 days",
           backtrace=True, diagnose=True,
           filter=__make_filter("debugger"))

system_logger = logger.bind(name="system")
exception_logger = logger.bind(name="server")
connection_logger = logger.bind(name="connection")
money_logger = logger.bind(name="money")
item_logger = logger.bind(name="item")
command_logger = logger.bind(name="command")
debugger = logger.bind(name="debugger")
