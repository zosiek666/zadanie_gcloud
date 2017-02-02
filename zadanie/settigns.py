import falcon
from zadanie.schemas import Test
from zadanie.personal import Personal
from zadanie.resources import TestowyResource, TestowyCollectionResource


CLIENT = 'testowy-157510'
KIND = 'Personal'
API = falcon.API()
PERSONAL_HANDLER = Personal(CLIENT, KIND)
TEST_SCHEMA_HANDLER = Test()
API.add_route('/', TestowyResource())
API.add_route('/{resource_name}', TestowyCollectionResource())
