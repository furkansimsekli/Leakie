import sys

import toml

config_path = sys.argv[1] if len(sys.argv) > 1 else 'config.toml'
config = toml.load(config_path)

API_KEY = config['API_KEY']
DB_STRING = config['DB_STRING']
WEBHOOK_URL = config['WEBHOOK_URL']

PROXY_LIST = config['PROXY_LIST']
