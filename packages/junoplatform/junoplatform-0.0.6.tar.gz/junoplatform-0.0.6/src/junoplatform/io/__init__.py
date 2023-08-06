__all__ = [
    'InputConfig', 
    'MongoOutput',
    'OPCOutput',
]

from pydantic import BaseModel, Field, root_validator
import datetime
from typing import Optional, Any, List

from junoplatform.io._output import MongoWriter, OPCWriter


class InputConfig(BaseModel):
    '''
    tags: OPC tags
    minutes: last n minutes of data
    items: last n records of data
    inteval: algo schedule interval in seconds
    '''
    tags: List[str]
    minutes: Optional[int] = Field(default=None, description="input data of last n minutes")
    items: Optional[int] = Field(default= None, description="input data of last n items")
    time_from: Optional[datetime.datetime] = Field(default= None, description="input data from time")
    time_to: Optional[datetime.datetime] =Field(default= None, description="input data to time")
    interval: int = Field(description="schedule interval in seconds")

    @root_validator
    def atleast_one(cls, values: "dict[str, Any]") -> "dict[str, Any]":
        if all([values.get("minutes"), values.get("items"), values.get("time_from")]):
            raise ValueError("field 'minutes' or 'items' must be given")
        return values
    

MongoOutput = MongoWriter()
OPCOutput = OPCWriter()
