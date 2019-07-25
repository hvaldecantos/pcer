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
                print(os.path.join(self.path, entry))
                y = yaml.load(open(os.path.join(self.path, entry)), Loader = yaml.SafeLoader)
                self.system_db.insert(y)
        self.system_db.remove(self.system.enabled == False)

    def getWarmupSystems(self):
        return self.system_db.search(self.system.warmup == True)

    def getExperimentalSystems(self):
        return self.system_db.search(self.system.warmup == False)
