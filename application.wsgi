#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname

sys.path.append('/home/yxm/bbs_and_blog/venv/lib/python3.4/site-packages')
sys.path.insert(0, abspath(dirname(__file__)))


from run import configured_app
application = configured_app()


