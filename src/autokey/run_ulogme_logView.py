#!/usr/bin/env python3
import os
import time

home = os.path.expanduser('~')

os.chdir('{}/.local/ulogme/scripts/'.format(home))

os.system('/usr/bin/python3 ./export_events.py &')

time.sleep(3)


os.system('/usr/bin/python3 ./ulogme_serve.py &')

time.sleep(0.2)

os.system('firefox http://localhost:8124 &')
