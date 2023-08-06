import os

"""Logger class for logging to a file"""
class FileLogger(object):

    @staticmethod
    def get_instance(self, filename):
        if not hasattr(self, '_instance'):
            self._instance = FileLogger(filename)
        return self._instance

    def __init__(self, filename):
        # Check if file exists
        if not os.path.exists(filename):
            # Create file
            open(filename, 'w').close()
        self.filename = filename

    def log(self, msg):
        with open(self.filename, 'a') as f:
            f.write(msg + '\n')
        f.close()
