import wegeh0mat_plugin
from  bot_client import BotClient

class MucPlugin(wegeh0mat_plugin.Wegeh0MatPlugin):
    
    def muc_command(self, msg):
        nick = self._config['nick']
        
        if msg['mucnick'] != nick \
         and msg['body'].strip().startswith(nick)\
         and msg['from'].bare == self._config['room']:
            self._notfiy_command_subscribers(self, msg, msg['body'].replace(nick, '').lstrip(' :,'), msg['mucnick'], None)
            
        
    def handle_reply(self, origmsg, message):
        self._botClient.send_message(mto=origmsg['from'].bare,
                          mbody=message, mtype='groupchat')
    
    
    def start(self, event):
        self._botClient.plugin['xep_0045'].joinMUC(self._config['room'], self._config['nick'], wait=True)    
    
    def __init__(self, config: 'dict with config options' , botClient : 'the BotClient instance to use'):
        super(MucPlugin, self).__init__(config, botClient)

        self._botClient.add_event_handler('session_start', self.start)
        botClient.add_event_handler('groupchat_message', self.muc_command)
    
