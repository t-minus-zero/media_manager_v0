import logging
import traceback
from colorama import Fore, Style

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Logger:
    def __init__(self, show_traceback=False, show_time=False):
        self.logger = logger
        self.show_traceback = show_traceback
        self.show_time = show_time

    def _get_time_prefix(self):
        if self.show_time:
            return f"{logging.Formatter('%(asctime)s', '%Y-%m-%d %H:%M:%S').format(logging.LogRecord(name='', level=logging.INFO, pathname='', lineno=0, msg='', args=(), exc_info=None))} - "
        return ""

    def log_error(self, source_name, error, force_traceback=False):
        time_prefix = self._get_time_prefix()
        self.logger.error(f"{time_prefix}{Fore.LIGHTRED_EX}ERROR from {source_name}:{Style.RESET_ALL} {str(error)}")
        if self.show_traceback or force_traceback:
            self.logger.error(f"{Fore.LIGHTRED_EX}{traceback.format_exc()}{Style.RESET_ALL}")

    def log_info(self, source_name, message):
        time_prefix = self._get_time_prefix()
        self.logger.info(f"{time_prefix}{Fore.LIGHTBLUE_EX}INFO from {source_name}:{Style.RESET_ALL} {message}")

    def log_warning(self, source_name, message):
        time_prefix = self._get_time_prefix()
        self.logger.warning(f"{time_prefix}{Fore.LIGHTYELLOW_EX}WARNING from {source_name}:{Style.RESET_ALL} {message}")

    def log_debug(self, source_name, message):
        time_prefix = self._get_time_prefix()
        self.logger.debug(f"{time_prefix}{Fore.LIGHTCYAN_EX}DEBUG from {source_name}:{Style.RESET_ALL} {message}")

    def log_success(self, source_name, message):
        time_prefix = self._get_time_prefix()
        self.logger.info(f"{time_prefix}{Fore.LIGHTGREEN_EX}SUCCESS from {source_name}:{Style.RESET_ALL} {message}")

    def log_response(self, source_name, message):
        time_prefix = self._get_time_prefix()
        self.logger.info(f"{time_prefix}{Fore.LIGHTMAGENTA_EX}RESPONSE from {source_name}:{Style.RESET_ALL} {message}")

# Create a module-level logger instance
log = Logger(show_traceback=False, show_time=False)

if __name__ == "__main__":
    try:
        1 / 0
    except Exception as e:
        log.log_error("example_script", e, force_traceback=True)
    
    log.log_info("example_script", "This is an informational message.")
    log.log_warning("example_script", "This is a warning message.")
    log.log_debug("example_script", "This is a debug message.")
    log.log_success("example_script", "This operation was successful.")
