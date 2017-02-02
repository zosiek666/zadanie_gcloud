import json
import falcon

from zadanie import settigns
from zadanie.logger import logger


class TestowyCollectionResource:
    def on_get(self, req, resp, resource_name=None):
        if resource_name:
            ent = settigns.PERSONAL_HANDLER.get_ent_by_name(resource_name)
            resp.body = json.dumps(settigns.TEST_SCHEMA_HANDLER.serialize(ent))
            if not ent:
                resp.status = falcon.HTTP_204
        else:
            resp.body = json.dumps({'entities': [settigns.TEST_SCHEMA_HANDLER.serialize(item) for item in
                                                 settigns.PERSONAL_HANDLER.get_all_ent()]})

    def on_put(self, req, resp, resource_name=None):
        if resource_name:
            try:
                json_parsed = json.load(req.stream)
            except Exception as ex:
                logger.exception(ex)
                resp.status = falcon.HTTP_400
                resp.body = json.dumps({'exception': '{}'.format(ex)})
            else:
                new_ent = settigns.TEST_SCHEMA_HANDLER.serialize(json_parsed)
                if new_ent['name'] != 'Not specific':
                    if settigns.PERSONAL_HANDLER.change_name_for_entity(resource_name, new_ent['name']):
                        resp.status = falcon.HTTP_201
                        resp.body = json.dumps({'entitie': new_ent['name']})
                    else:
                        resp.status = falcon.HTTP_422
                        resp.body = json.dumps({'code': 'API0x41'})
                else:
                    resp.body = json.dumps({'name': 'required'})
                    resp.status = falcon.HTTP_400
        else:
            resp.body = json.dumps({'resource_name': 'required'})
            resp.status = falcon.HTTP_400


class TestowyResource(TestowyCollectionResource):
    def on_post(self, req, resp):
        try:
            json_parsed = json.load(req.stream)
        except Exception as ex:
            logger.exception(ex)
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'exception': '{}'.format(ex)})
        else:
            new_ent = settigns.TEST_SCHEMA_HANDLER.serialize(json_parsed)
            if new_ent['name'] != 'Not specific':
                if settigns.PERSONAL_HANDLER.add_or_increment_ent(new_ent):
                    resp.status = falcon.HTTP_201
                    resp.body = json.dumps({'entitie': new_ent['name']})
                else:
                    resp.status = falcon.HTTP_422
                    resp.body = json.dumps({'code': 'API0x59'})
            else:
                resp.body = json.dumps({'name': 'required'})
                resp.status = falcon.HTTP_400
