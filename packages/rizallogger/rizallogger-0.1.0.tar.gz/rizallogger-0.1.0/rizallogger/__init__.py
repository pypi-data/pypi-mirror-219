import logging


class Log:

    def __init__(self, fileName) -> None:
        self.filename = fileName

        self.format = "%(asctime)s :: %(levelname)s :: %(message)s"
        self.logger = logging.getLogger(__name__)

        # handler
        self.stream_h = logging.StreamHandler()
        self.file_h = logging.FileHandler(self.filename)

        # level
        self.stream_h.setLevel(logging.WARNING)
        self.stream_h.setLevel(logging.ERROR)

        # formatter
        self.formatter = logging.Formatter(self.format)
        self.stream_h.setFormatter(self.formatter)
        self.file_h.setFormatter(self.formatter)

        # addhandler
        self.logger.addHandler(self.stream_h)
        self.logger.addHandler(self.file_h)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.warning(message)
