#!/usr/bin/env python3
from os.path import split
import mcs
callLog = getattr(mcs, 'executeScript')(split(__file__)[1].replace('.py', ''))
