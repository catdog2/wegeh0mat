import wegeh0mat_plugin
from  bot_client import BotClient

class DirectChatPlugin(wegeh0mat_plugin.Wegeh0MatPlugin):
    def handle_reply(self, origmsg, message):
        self._botClient.send_message(mto=origmsg['from'].bare,
                          mbody=message, mtype=origmsg["type"])
    
    def _message(self, msg):
        if msg['type'] in ('chat', 'normal'):    
            self._notfiy_command_subscribers(self, msg, msg['body'], msg['from'].bare.split("@")[0], msg['from'].bare)
     
    
    def __init__(self, config: 'dict with config options' , botClient : 'the BotClient instance to use'):
        super(DirectChatPlugin, self).__init__(config, botClient)

        
        
        botClient.add_event_handler("message", self._message)
    
