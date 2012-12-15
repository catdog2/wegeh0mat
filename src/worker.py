import abc

class Worker(object):

    __metaclass__ = abc.ABCMeta
    
    def __init__(self, config):
        self._config = config
        
    @abc.abstractmethod
    def handle_command(self, datadict):
        return