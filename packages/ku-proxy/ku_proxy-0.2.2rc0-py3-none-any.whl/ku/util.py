"""
    ## Misc
"""

import logging, os
os.system('color')
from typing import Optional, Tuple
from threading import Lock, get_ident

class CustomFormatter(logging.Formatter):    
    
    grey = '\u001b[34m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\u001b[31m'
    reset = '\x1b[0m'    

    def __init__(self, fmt, primary: Optional[str] = blue):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: primary + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%m/%d/%Y %I:%M:%S %p')
        return formatter.format(record)

def split(a, n):
    k, m = divmod(len(a), n)
    return [a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n)]

def genrancol(brightness: int = 1) -> Tuple[int, int, int]:
    cs = os.urandom(1)[0], os.urandom(1)[0], os.urandom(1)[0]
    while cs[0] + cs[1] + cs[2] < 250:
        cs = os.urandom(1)[0], os.urandom(1)[0], os.urandom(1)[0]
    r, g, b = (min(255, int(c * brightness)) for c in cs)
    return r, g, b

def ansicol(r: int, g: int ,b: int) -> str:
    return f"\x1b[38;2;{r};{g};{b}m"

def flock(fun, data = {}):
    data[hash(fun)] = [Lock()]

    def wrapper(*args, **kwargs):
        with data[hash(fun)][0]:
            return fun(get_ident(), *args, **kwargs)

    return wrapper

def format_bytes(size):
    """
        https://stackoverflow.com/questions/12523586/python-format-size-application-converting-b-to-kb-mb-gb-tb
    """
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'B'
