import logging
import os

class Logger(object):
    def __init__(self, log_path):
        """create a logger object

        Args:
            log_path (str): the path of the log file
        """
        try:
            with open(log_path, "w") as f:
                pass
        except:
            directory = os.path.dirname(log_path)
            os.makedirs(directory)
            with open(log_path, "w") as f:
                pass
        # set the logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(filename)s - %(lineno)d - %(levelname)s: - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        # use FileHandler to output to the log
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)

        # use StreamHandler to output to the console
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)

        # add the handler to the logger
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)