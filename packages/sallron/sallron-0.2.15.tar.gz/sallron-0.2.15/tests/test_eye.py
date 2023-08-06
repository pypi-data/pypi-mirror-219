from sallron.eye import *
from sallron.util import settings
from os import environ

MOCK_CUSTOMER = 'fibracirurgica'
MOCK_INFO_DICT = dict(vtex_interface = dict(app_key=environ.get('VTEX_TEST_APP_KEY'),
app_token=environ.get('VTEX_TEST_APP_TOKEN'),
environment="vtexcommercestable",
account_name="fibracirurgica", 
local_tz="America/Sao_Paulo"))
MOCK_INTERFACE_NAME = 'vtex_interface'
MONGO_TEST_STR = environ.get('MONGO_TEST_CONN_STR')

class MockInterface():
    def __init__(self,app_key,app_token,environment,account_name,local_tz):
        self.mock_interface = account_name

class MockMongo():
    def insert_data(self, collection, db, data):
        self.database = dict(db=dict(collection=dict(data)))

def mock_function(period):
    pass

def test_eye_class_init():
    TheEyeofSauron(MOCK_CUSTOMER,MOCK_INFO_DICT, MockInterface, MOCK_INTERFACE_NAME)

def test_configureye():
    configureye(MOCK_SETTING='Pterodatilo')
    assert settings.MOCK_SETTING == 'Pterodatilo'

def test_fetch_and_store():
    methods = filter(mock_function, ['steffen', 'chris'])
    client = TheEyeofSauron(MOCK_CUSTOMER,MOCK_INFO_DICT, MockInterface, MOCK_INTERFACE_NAME)
    for method in methods:
        client.fetch_and_store(method, 15, MockMongo)

def test_setup_schedulers():
    client = TheEyeofSauron(MOCK_CUSTOMER,MOCK_INFO_DICT, MockInterface, MOCK_INTERFACE_NAME)
    client.setup_schedulers(dict(name='george'), MockMongo)

# def test_ring_ruler():
#     configureye(MONGO_CONN_STR=MONGO_TEST_STR)
#     ring_ruler(MockInterface, MOCK_INTERFACE_NAME, test=True)
