import logging
import logging.config


class ColorFormatter(logging.Formatter):

    def format(self, record):
        return


class TopicPublisher():

    def __init__(self):
        pass

    def set_publisher(self, app_id, publisher):
        pass

    def publish(self, timestamp, logger_name, level, message):
        pass


topic_publisher = TopicPublisher()


class RaYaLogger():

    def __init__(self, name: str):
        self.py_logger = logging.getLogger(self.__name)

    def debug(self, message):
        pass

    def info(self, message):
        pass

    def warn(self, message):
        pass

    def warning(self, message):
        pass

    def error(self, message):
        pass

    def critical(self, message):
        pass

    def fatal(self, message):
        pass


__deprecation_logger = RaYaLogger('Deprecation Notice')
__debug_warning_logger = RaYaLogger('Debug')


def DEPRECATION_WARNING(msg):
    pass


def DEPRECATION_NEW_METHOD(new_method_name):
    pass


def DEBUG_WARNING(msg):
    pass
