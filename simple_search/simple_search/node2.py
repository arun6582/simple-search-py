import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


from settings import *

nodename = 'node2'

DB_SETTINGS = {
    'node': 'node2',
    'path': os.path.join(BASE_DIR, 'dbdata', nodename),
    'othernodes': {
    }
}
