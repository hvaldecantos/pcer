from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage
import os, fnmatch
import json
import random
import yaml

class Resource():
    system_db = None
    system = None

    def __init__(self):
        config = yaml.load(open("config.yml"), Loader = yaml.SafeLoader)
        self.path = config['resource']
        self.system_db = TinyDB(storage = MemoryStorage)
        self.system = Query()
        self.setSystemDB()

    def setSystemDB(self):
        listOfFiles = os.listdir(self.path)
        pattern = "*.yml"
        for entry in listOfFiles:
            if fnmatch.fnmatch(entry, pattern):
                y = yaml.load(open(os.path.join(self.path, entry)), Loader = yaml.SafeLoader)
                self.system_db.insert(y)
        self.system_db.remove(self.system.enabled == False)

    def getWarmupSystems(self):
        return self.system_db.search(self.system.warmup == True)

    def getExperimentalSystems(self):
        return self.system_db.search(self.system.warmup == False)

    def getGroups(self):
        return [file for file in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, file)) and not file[0] == '.' ]

    def getSystem(self, system_id):
        try:
            return self.system_db.search(self.system.id == system_id)[0]
        except IndexError:
            raise Exception("System with 'id': '%s' not found." % system_id)

    def getTaks(self):
        pass
