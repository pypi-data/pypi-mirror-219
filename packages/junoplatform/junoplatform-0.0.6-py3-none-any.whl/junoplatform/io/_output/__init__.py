from abc import ABC, abstractmethod
import logging
from decouple import config as dcfg

class Writer(ABC):
    @abstractmethod
    def write(self, data: dict, table:str = ""):
        pass
    
class MongoWriter(Writer):
    def __init__(self, **kwargs):
        super(MongoWriter, self).__init__()
        self.url = dcfg("MONGO_URL", "mongodb://root:L0veMongo23@192.168.101.157:27017")
        self.plant = dcfg("PLANT", "gangqu")

    def write(self, data: dict, table: str,):
        logging.info(f"written data to mongo {self.plant}.{table}: {data}")

class OPCWriter(Writer):
    def __init__(self, **kwargs):
        super(OPCWriter, self).__init__()
        self.plant = dcfg("PLANT", "gangqu")

    def write(self,  data: dict):
        logging.info(f"written data to OPC {self.plant}: {data}")
            