import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from settings import *

nodename = 'node1'

DB_SETTINGS = {
    'node': nodename,
    'path': os.path.join(BASE_DIR, 'dbdata', nodename),
    'othernodes': [
        'http://localhost:8001'
    ]
}
