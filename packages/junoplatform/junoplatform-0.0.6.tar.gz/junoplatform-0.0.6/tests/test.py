from junoplatform.meta.decorators import EntryPoint
from junoplatform.io import *
import logging
import random

#@EntryPoint(InputConfig(tags=["OPC_TAG1", "OPC_TAG2"], items=1440, interval=5), detached=False)
@EntryPoint("input.json", detached=False)
def any_algo_entry_func(data):
    '''
    data: numpy.ndarray
      it is automatically provided by the junoplatform framework, and its content is specified by `InputConfig` above
    '''

    # TODO: algo processing with input data here
    logging.info(f"processing data: {data.shape}")
    
    # TODO: construct results as dict
    opc_data = {"OPC_TAG1": random.randint(1,10), "OPC_TAG2": random.randint(1,10)}
    probe1 = {"out":random.randint(1,10)}

    # TODO: algo oputput results
    logging.info("data processed, writing outputs:")
    MongoOutput.write(probe1, "probe1")
    OPCOutput.write(opc_data)