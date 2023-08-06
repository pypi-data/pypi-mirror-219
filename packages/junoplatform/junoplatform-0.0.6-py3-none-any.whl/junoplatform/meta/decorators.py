import numpy as np
from threading import Thread
from junoplatform.io import InputConfig
from functools import wraps
import datetime
import time
import logging
import os
import json

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s - %(message)s')
class EntryPoint:
    def __init__(self, cfg_in: str|InputConfig, detached: bool = False):
        super(EntryPoint, self).__init__()
        self.cfg_in: InputConfig
        self.detached = detached
        if isinstance(cfg_in, str):
            self.cfg_in = InputConfig(**json.load(open(cfg_in)))
        elif isinstance(self.cfg_in, InputConfig):
            self.cfg_in = cfg_in
        else:
            raise Exception(f"cfg_in must be type of InputConfig or string, but provides: {type(self.cfg_in)}")

    def __call__(self, func):
        def thread():
           while True:
              # TODO: prepare data for func
              # mock data
              ts = datetime.datetime.now().timestamp()
              row = len(self.cfg_in.tags)
              col = self.cfg_in.items
              
              data = np.zeros((row, col)) # type: ignore
              func(data)
              # TODO: output
              te = datetime.datetime.now().timestamp()

              delay = self.cfg_in.interval - (te -ts) - 0.003
              logging.info(f"delay: {delay}")
              if delay < 0: 
                 delay = 0
              time.sleep(delay)
              
        th = Thread(target=thread)
        if self.detached:
            th.daemon = True
        th.start()
        if not self.detached:
            th.join()
        


def auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not os.path.exists(args[0].juno_dir) or not os.path.exists(args[0].juno_file):
            # TODO: auth token
            logging.error(f"user not authenticationd.")
            logging.error(f"please run `junocli setup <username> <password>` to use your shuhan account")
            os.makedirs(args[0].juno_dir, exist_ok=True)
            return -1
        return func(*args, **kwargs)
        
    return wrapper