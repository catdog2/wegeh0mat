import wegeh0mat_plugin
from  bot_client import BotClient

class MucPlugin(wegeh0mat_plugin.Wegeh0MatPlugin):

    
    def muc_message(self, msg):
        if msg['mucnick'] != self._config['nick'] and \
             self._config['nick'] in msg['body'] and  \
             msg['from'].bare == self._config['room']:
             
            #   self.botClient.send_message(mto=msg['from'].bare, mbody='Hey you ' + 
            #                     msg['mucnick'] + ' it seems you said: ' + msg['body'], mtype='groupchat')
            
            datadict = {}
            datadict['from'] = msg['from'].bare
            datadict['mucnick'] = msg['mucnick']
            datadict['message'] = msg['body']
            
            print(msg)
             
            self._notfiy_command_subscribers(datadict)
    
    
    def start(self, event):
        self._botClient.plugin['xep_0045'].joinMUC(self._config['room'], self._config['nick'], wait=True)    
    
    def __init__(self, config: 'dict with config options' , botClient : 'the BotClient instance to use'):
        super(MucPlugin, self).__init__(config, botClient)
        self.botClient = botClient
        
        self._botClient.add_event_handler('session_start', self.start)
        botClient.add_event_handler('groupchat_message', self.muc_message)
    
