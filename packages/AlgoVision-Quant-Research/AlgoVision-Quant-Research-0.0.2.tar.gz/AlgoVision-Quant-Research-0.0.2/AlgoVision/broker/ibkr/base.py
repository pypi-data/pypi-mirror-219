# Base Class for IBKR

from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
from ibapi.contract import *
from ibapi.ticktype import *
from ibapi.order import *
from ibapi.order_state import *

class Base_IBKR(EClient, EWrapper):
    """ Base class for IBKR

    """

    def __init__(self):
        EClient.__init__(self, self)

