import abc
import sqlite3

class Worker(object):

    __metaclass__ = abc.ABCMeta
    
    def __init__(self, config):
        self._config = config
        
    @abc.abstractclassmethod
    def handle_command(self, origin, msg, command, sendername, senderjid: str):
        '''
        returns response or None if no response
        
        :param msg: orig message
        :param command: the command string
        '''
        return