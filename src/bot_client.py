#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getpass
import sleekxmpp

class BotClient(sleekxmpp.ClientXMPP):
    
    def load_plugin(self, options  , plugin_class):
        '''
        returns created plugin instance
        
        :param options: option dict for plugin
        :param plugin_class: plugin class object
        '''
        
        loaded_plugin = plugin_class(options, self)
        self.__loaded_plugins.append(loaded_plugin)
        return loaded_plugin

    @property
    def loaded_plugins(self):
        return list(self.__loaded_plugins)
    
    def post_message(self, to, message):
        return
    
    def add_command_subscriber(self, function):
        for i in self.__loaded_plugins:
            i.add_command_subscriber(function)
    
    def muc_subject(self, msg):
         self.send_message(mto=msg['from'].bare, mbody=str(msg['from']), mtype='groupchat')
    
    
    def __init__(self, jid, password):
        self.__loaded_plugins = []
        
        super(BotClient, self).__init__(jid, password)
        
        #loading plugins
        self.register_plugin('xep_0030')  # serivce d
        self.register_plugin('xep_0199')  # ping
        self.register_plugin('xep_0004')  # Data Forms
        self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0045')  # muc
        
        self.add_event_handler('session_start', self.start)
        #self.add_event_handler("muc::%s::got_online" % self.room, self.muc_online)
        #self.add_event_handler('groupchat_subject' , self.muc_subject)
        
    def muc_online(self, presence):
        if presence['muc']['nick'] != self.nick:
            self.send_message(mto=presence['from'].bare,
                          mbody="Hello, %s %s %s" % (presence['muc']['affiliation'],
                                                  presence['muc']['role'],
                                                  presence['muc']['nick']),
                          mtype='groupchat')
            
            
    
    def start(self, event):
        self.send_presence()
        self.get_roster()
        
        
'''Here we will create out echo bot class'''
        
    
    

