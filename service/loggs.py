import logging
import os


class Loggs:

    def __init__(self, level=logging.INFO, nome_logger="loggs"):
        self.logger = logging.getLogger(nome_logger)
        self.set_level(level)

    def set_level(self, level):
        # Remove existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        log_filepath = "export"
        os.makedirs(log_filepath, exist_ok=True)

        level_name = logging.getLevelName(level).lower()
        file_name = f"{level_name}.log"
        log_fullpath = os.path.join(log_filepath, file_name)
        self.logger.setLevel(level)

        # Formatter ("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        formatter = logging.Formatter("%(message)s", datefmt="%H:%M:%S")

        # File handler
        file_handler = logging.FileHandler(log_fullpath, encoding="UTF-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # Always log DEBUG level to console
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
