import os

CONFIGS = {}

CONFIGS['TEST'] = {
    'connection_string': 'sqlite:////tmp/test.db',
    'secret_key': 'test',
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True,
    'env': 'TEST',
}

CONFIGS['DEV'] = {
    'connection_string': 'sqlite:///' + os.getcwd() + '/dev.db',
    'secret_key': 'dev',
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True,
    'env': 'DEV',
}


def get_config(env=None):
    # No argument given
    if env is None:
        env = os.environ.get('ENV')

    # Environment is invalid
    if env not in CONFIGS.keys():
        env = 'DEV'

    return CONFIGS[env]
