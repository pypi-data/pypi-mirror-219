import pprint

from dev.dev_setup import load_dev_environment
from fxpyD365api import GenericWrapper

load_dev_environment()

data = {
    "title": "Created from test 6",
    "description": "Example short description",
    "customerid_account@odata.bind": "/accounts(334e12ea-c34c-ea11-b698-00155d56d687)"
}


inc = GenericWrapper('incidents')

r = inc.create(data)
print(r)
pprint.pprint(r.json())
