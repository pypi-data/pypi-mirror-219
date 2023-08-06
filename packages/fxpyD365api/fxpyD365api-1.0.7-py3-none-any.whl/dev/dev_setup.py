import json
import os


def load_dev_environment():
    if os.path.exists('develop-environment.json'):
        environment_dict = json.loads(open('develop-environment.json', 'r').read())
        for key, value in environment_dict.items():
            if key.upper() == key:
                os.environ[key] = value
