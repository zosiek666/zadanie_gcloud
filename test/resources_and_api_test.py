import os
import sys
from falcon import testing
import falcon
import pytest
import json

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from zadanie.personal import Personal
from zadanie.settigns import API

ONE_ENTITY = {'name': 'Kamil', 'count': 3}
ENTITIES = [{'name': 'Kamil', 'count': 3}, {'name': 'Andff', 'count': 1}, {'name': 'asd', 'count': 4}]
ENTITIES_ALL_RESPONSE = {
    'entities': [{'count': '3', 'name': 'Kamil'}, {'count': '1', 'name': 'Andff'}, {'count': '4', 'name': 'asd'}]}
ENTITY_RESPONSE = {'name': 'Kamil', 'count': 3}
ONE_ENTITY_RESPONSE = {'name': 'Kamil', 'count': '3'}
POST_AND_PUT_JSON = {'name': 'Andrzej'}
BAD_POST_AND_PUT_JSON = {"Name": "Andrzej"}
EXEPTION_NO_JSON = {'exception': 'Expecting value: line 1 column 1 (char 0)'}
NO_RESOURCES_NAME = {'resource_name': 'required'}
NO_NAME = {'name': 'required'}
HEADERS = {"Content-Type": "application/json"}
GOOD_ENITYT_RESPONSE = {'entitie': 'Andrzej'}
CODE_API_59 = {'code': 'API0x59'}
CODE_API_41 = {'code': 'API0x41'}


@pytest.fixture(scope='module')
def client():
    return testing.TestClient(API)


def test_get_main(client, mocker):
    mocker.patch.object(Personal, 'get_all_ent')
    Personal.get_all_ent.return_value = ENTITIES
    resp = client.simulate_get('/')
    assert resp.status == falcon.HTTP_OK
    assert resp.json == ENTITIES_ALL_RESPONSE


def test_get_entity(client, mocker):
    mocker.patch.object(Personal, 'get_ent_by_name')
    Personal.get_ent_by_name.return_value = ONE_ENTITY
    resp = client.simulate_get('/Kamil')
    assert resp.status == falcon.HTTP_OK
    assert resp.json == ONE_ENTITY_RESPONSE


def test_get_not_existing_entity(client, mocker):
    mocker.patch.object(Personal, 'get_ent_by_name')
    Personal.get_ent_by_name.return_value = {}
    resp = client.simulate_get('/Asd')
    assert resp.status == falcon.HTTP_204


def test_post_main_no_params(client, mocker):
    mocker.patch.object(Personal, 'add_or_increment_ent')
    resp = client.simulate_post('/')
    assert resp.status == falcon.HTTP_400
    assert resp.json == EXEPTION_NO_JSON


def test_put_main(client, mocker):
    mocker.patch.object(Personal, 'change_name_for_entity')
    Personal.change_name_for_entity.return_value = True
    resp = client.simulate_put('/', body=json.dumps(BAD_POST_AND_PUT_JSON), headers=HEADERS)
    assert resp.status == falcon.HTTP_400
    assert resp.json == NO_RESOURCES_NAME


def test_put_enity_no_params(client, mocker):
    mocker.patch.object(Personal, 'change_name_for_entity')
    Personal.change_name_for_entity.return_value = True
    resp = client.simulate_put('/Kamil')
    assert resp.status == falcon.HTTP_400
    assert resp.json == EXEPTION_NO_JSON


def test_put_main_bad_params(client, mocker):
    mocker.patch.object(Personal, 'change_name_for_entity')
    Personal.change_name_for_entity.return_value = True
    resp = client.simulate_put('/Kamil', body=json.dumps(BAD_POST_AND_PUT_JSON), headers=HEADERS)
    assert resp.status == falcon.HTTP_400
    assert resp.json == NO_NAME


def test_put_enity_proper(client, mocker):
    mocker.patch.object(Personal, 'change_name_for_entity')
    Personal.change_name_for_entity.return_value = True
    resp = client.simulate_put('/Kamil', body=json.dumps(POST_AND_PUT_JSON), headers=HEADERS)
    assert resp.status == falcon.HTTP_201
    assert resp.json == GOOD_ENITYT_RESPONSE


def test_put_enity_not_exists(client, mocker):
    mocker.patch.object(Personal, 'change_name_for_entity')
    Personal.change_name_for_entity.return_value = False
    resp = client.simulate_put('/Kamil', body=json.dumps(POST_AND_PUT_JSON), headers=HEADERS)
    assert resp.status == falcon.HTTP_422
    assert resp.json == CODE_API_41


def test_post_enity(client, mocker):
    mocker.patch.object(Personal, 'change_name_for_entity')
    Personal.change_name_for_entity.return_value = True
    resp = client.simulate_post('/Kamil', body=json.dumps(POST_AND_PUT_JSON), headers=HEADERS)
    assert resp.status == falcon.HTTP_405


def test_post_main_bad_params(client, mocker):
    mocker.patch.object(Personal, 'add_or_increment_ent')
    Personal.add_or_increment_ent.return_value = True
    resp = client.simulate_post('/', body=json.dumps(BAD_POST_AND_PUT_JSON), headers=HEADERS)
    assert resp.status == falcon.HTTP_400
    assert resp.json == NO_NAME


def test_post_main(client, mocker):
    mocker.patch.object(Personal, 'add_or_increment_ent')
    Personal.add_or_increment_ent.return_value = True
    resp = client.simulate_post('/', body=json.dumps(POST_AND_PUT_JSON), headers=HEADERS)
    assert resp.status == falcon.HTTP_201
    assert resp.json == GOOD_ENITYT_RESPONSE


def test_post_main_again_error(client, mocker):
    mocker.patch.object(Personal, 'add_or_increment_ent')
    Personal.add_or_increment_ent.return_value = False
    resp = client.simulate_post('/', body=json.dumps(POST_AND_PUT_JSON), headers=HEADERS)
    assert resp.status == falcon.HTTP_422
    assert resp.json == CODE_API_59
