import wegeh0mat_plugin
from  bot_client import BotClient

class MucEchoPlugin(wegeh0mat_plugin.Wegeh0MatPlugin):

    
    def muc_message(self, msg):
        if msg['mucnick'] != self.botClient.nick and self.botClient.nick in msg['body']:
            self.botClient.send_message(mto=msg['from'].bare, mbody='Hey you ' + 
                              msg['mucnick'] + ' it semms you said: ' + msg['body'], mtype='groupchat')
    
    
    def __init__(self, config: 'dict with config options' , botClient : 'the BotClient instance to use'):
        super(EchoPlugin, self).__init__(config, botClient)
        self.botClient = botClient
        
        print(config)
        
        botClient.add_event_handler('groupchat_message', self.muc_message)
    