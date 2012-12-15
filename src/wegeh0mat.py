from optparse import OptionParser
import sys
import logging
from bot_client import BotClient
from wegeh0mat_plugin import Wegeh0MatPlugin
from confparser import ConfigParser

if __name__ == '__main__':
    
    '''Here we will configure and read command line options'''
    optp = OptionParser()
    optp.add_option('-d', '--debug' , help='set logging to DEBUG', action='store_const', dest='loglevel')
    
    opts, args = optp.parse_args()
    
    logging.basicConfig(level="DEBUG", format='%(levelname)-8s %(message)s')
    

    config = ConfigParser("config.xml")
    concfgs = config.get_connection_config_list()
    workers = config.init_worker_instances()
    
    botClientlist = []
    for c in concfgs:
        bc = BotClient(c['jid'], c['password'])
        config.init_plugin_instances(bc) # init plugins
        botClientlist.append(bc)
        
        ## register subscribe workers
        for w in workers:
            bc.add_command_subscriber(w.handle_command)
        
        if(bc.connect()):
            bc.process()
        else:
            print('can\'t connect!')

