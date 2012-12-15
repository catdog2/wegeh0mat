from xml.dom.minidom import parse, parseString
import importlib

class ConfigParser(object):
    def __init__(self, filename):
        self.__dom = parse(filename)  # parse an XML file by name

    def __class_for_name(self, module_name, class_name):
        # load the module, will raise ImportError if module cannot be loaded
        m = importlib.import_module(module_name)
        # get the class, will raise AttributeError if class cannot be found
        c = getattr(m, class_name)
        return c

    def get_connection_config_list(self) -> "a list of dicts":
        config = self.__dom.getElementsByTagName("config")[0]
        connections = config.getElementsByTagName("connections")[0]
        conlist = connections.getElementsByTagName("connection")
        
        reslist = []
        
        for i in conlist:
            d = {"jid" : i.attributes['jid'].value}
            for j in i.getElementsByTagName("option"):
                d[j.attributes['name'].value] = j.firstChild.nodeValue
            
            reslist.append(d)
            
        return reslist
    
    def init_plugin_instances(self, botClient):
        return_values = []
        
        config = self.__dom.getElementsByTagName("config")[0]
        plugins = config.getElementsByTagName("plugins")[0]
        pluginlist = plugins.getElementsByTagName("plugin")
        
        for plugin in pluginlist:
            for instance in plugin.getElementsByTagName("instance"):
                c = self.__class_for_name(plugin.attributes['package'].value + '.' + 
                                          plugin.attributes['module'].value,
                                          plugin.attributes['class'].value)
                                           
                
                if(botClient.boundjid.bare == instance.attributes['jid'].value):
                    opts = {}
                    for opt in instance.getElementsByTagName("option"):
                         opts[opt.attributes['name'].value] = opt.firstChild.nodeValue
                    
                    botClient.load_plugin(opts, c)
                    
    def init_worker_instances(self):
        config = self.__dom.getElementsByTagName("config")[0]
        workers = config.getElementsByTagName("workers")[0]
        workerlist = workers.getElementsByTagName("worker")
        
        workerret = []
        
        for worker in workerlist:
            w = self.__class_for_name(worker.attributes['package'].value + '.' + 
                                          worker.attributes['module'].value,
                                          worker.attributes['class'].value)
             
            opts = {}
            for opt in worker.getElementsByTagName("option"):
                opts[opt.attributes['name'].value] = opt.firstChild.nodeValue
                    
                workerret.append(w(opts))
        
        return workerret
             
        
        
            
