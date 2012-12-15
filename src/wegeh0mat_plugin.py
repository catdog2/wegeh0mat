import logging

class Wegeh0MatPlugin(object):
    '''
    Base class for plugins
    '''
    
    def __init__(self, config: 'dict with config options' , botClient : 'the BotClient instance to use'):
        logging.getLogger().info("loading plugin: %s",self.__class__.__name__)
        self._botClient = botClient 
        self._config = config