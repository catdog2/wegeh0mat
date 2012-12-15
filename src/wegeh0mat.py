from optparse import OptionParser
import sys
import logging
from bot_client import BotClient
from wegeh0mat_plugin import Wegeh0MatPlugin
from plugin_manager import PluginManager
from confparser import ConfigParser

if __name__ == '__main__':
    
    '''Here we will configure and read command line options'''
    optp = OptionParser()
    optp.add_option('-d', '--debug' , help='set logging to DEBUG', action='store_const', dest='loglevel')
    
    opts, args = optp.parse_args()
    
    if opts.jid is None:
        opts.jid = 'wegeh0mat@tuxzone.org'
    if opts.password is None:
        opts.password = 'wegeh0mat'
    if opts.plugins is None:
        opts.plugins = 'test_plugin.TestPlugin,echo_plugin.EchoPlugin'
        


    
    logging.basicConfig(level="DEBUG", format='%(levelname)-8s %(message)s')
    

    config = ConfigParser("config.xml")
    concfgs = config.get_connection_config_list()
    
    botClientlist = []
    for c in concfgs:
        bc = BotClient(c['jid'], c['password'])
        config.init_plugin_instances(bc) # init plugins
        botClientlist.append(bc)
        
        if(bc.connect()):
            bc.process(block=True)
        else:
            print('can\'t connect!')

    
    """
    xmpp = BotClient(opts.jid, opts.password, "test@conference.tuxzone.org", "wegeh0mat")
    
    pluginManager = PluginManager(xmpp)
    plugins = [i.split(".") for i in opts.plugins.split(",")]
    for i in plugins:
        pluginManager.add_plugin( class_for_name("wegeh0mat_plugins." + i[0], i[1]))
    
    '''Finally, we connect the bot and start listening for messages'''
    
    if(xmpp.connect()):
        xmpp.process(block=True)
    else:
        print('can\'t connect!')
    """