import logging
import uuid

class AppLogger:
    logger: logging.Logger
    id: str = None
    def __init__(self, name: str, id: str = str(uuid.uuid4())):
        self.logger = logging.getLogger(name)
        self.id = id
    
    def info(self, message: str, *args):
        self.logger.info(f"[{self.id}] " + message, *args)
    def error(self, message: str, *args):
        self.logger.error(f"[{self.id}] " + message, *args)
    def debug(self, message: str, *args):
        self.logger.debug(f"[{self.id}] " + message, *args)
    def warning(self, message: str, *args):
        self.logger.warning(f"[{self.id}] " + message, *args)
    def critical(self, message: str, *args):
        self.logger.critical(f"[{self.id}] " + message, *args)