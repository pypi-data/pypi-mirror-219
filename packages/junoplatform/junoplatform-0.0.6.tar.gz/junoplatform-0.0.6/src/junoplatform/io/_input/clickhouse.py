from junoplatform.io._input.reader import Reader
from urllib.parse import urlparse

class ClickHouseReader(Reader):
    '''
    clickhouse reader
    kwargs:
      url: optional. default = "ch://default:L0veClickhouse@host:9000"
    '''
    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        if not self.url:
            self.url = "ch://default:L0veClickhouse@host:9000"
            