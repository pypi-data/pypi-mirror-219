from datetime import datetime, time
from time import time


class TimeUtils(object):

    @staticmethod
    def get_instance(self):
        if not hasattr(self, '_instance'):
            self._instance = TimeUtils()
        return self._instance

    def __init__(self):
        pass

    # Returns the current time in the format: YYYY-MM-DD HH:MM:SS
    @staticmethod
    def get_current_time():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Returns the current time in milliseconds
    @staticmethod
    def get_current_time_millis():
        return int(round(time() * 1000))

    # Returns the current time in the format: YYYY-MM-DD
    @staticmethod
    def get_current_date():
        return datetime.now().strftime("%Y-%m-%d")

    # Formats the given time in milliseconds to the format: YYYY-MM-DD HH:MM:SS
    @staticmethod
    def format_time_millis(time_millis):
        return datetime.fromtimestamp(time_millis / 1000).strftime("%Y-%m-%d %H:%M:%S")
