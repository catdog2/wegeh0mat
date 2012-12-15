import abc

class Worker(object):

    __metaclass__ = abc.ABCMeta
    
    def __init__(self, config):
        self._config = config
        
    @abc.abstractmethod
    def handle_command(self, origin ,datadict):
        '''
        returns response or None if no response
        
        :param datadict:
        '''
        return