
class Wegeh0MatPlugin(object):
    
    def __init__(self, pluginConfig: 'dict with config options' , botClient : 'the BotClient instance to use'):
        self._botClient = botClient 
        self._pluginConfig = pluginConfig