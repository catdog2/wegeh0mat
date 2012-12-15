import worker
import logging

class WeggehWorker(worker.Worker):
    def __init__(self, config):
        super(WeggehWorker, self).__init__(config)
        
    def handle_command(self, datadict):
        return