import logging
import abc
import threading

class Wegeh0MatPlugin(object):
    '''
    Base class for plugins
    '''
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, config: 'dict with config options' , botClient : 'the BotClient instance to use'):
        logging.getLogger().info("loading plugin: %s", self.__class__.__name__)
        self._botClient = botClient 
        self._config = config
        self._message_subscribers = []
    
    def add_command_subscriber(self, function):
        '''
        adds subscribers for commands
        
        :param function: function to be called on notify
        '''
        
        self._message_subscribers.append(function)
    
    def _notfiy_command_subscribers(self, origin, msg, command, sendername :str, senderjid: str):
        for i in self._message_subscribers:
            i(origin, msg, command, sendername, senderjid)

    @abc.abstractclassmethod
    def handle_reply(self, origmsg, message):
        pass
