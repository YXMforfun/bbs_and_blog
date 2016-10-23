#import run as bbs

#app = bbs.configured_app()

# gunicorn appcorn:app
# nohup gunicorn -b '0.0.0.0:80' appcorn:app &

# wsgi

import sys
from os.path import dirname
from os.path import abspath
if __name__ == '__main__':
    print(__file__, dirname(__file__), abspath(dirname(__file__)))
