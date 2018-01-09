__author__ = 'Raman Pandey'
from uuid import getnode as get_mac

class getMac():
    def __init__(self):
        pass

    def mac_val(self):
        return hex(get_mac())[2:-1]

