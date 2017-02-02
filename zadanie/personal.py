from google.cloud import datastore
from zadanie.logger import logger


class Personal:
    def __init__(self, client, kind):
        self._client = client
        self._kind = kind
        self._ds = datastore.Client(self._client)

    def get_all_ent(self):
        if self._ds:
            query = self._ds.query(kind=self._kind)
            try:
                entities = list(query.fetch())
            except Exception as ex:
                logger.exception(ex)
                return []
            else:
                return entities
        else:
            return []

    def _save_entity(self, ent):
        if self._ds:
            try:
                self._ds.put(ent)
            except Exception as ex:
                logger.exception(ex)
                return False
            else:
                logger.info("Entity: {} saved to DB".format(ent['name']))
                return True
        return False

    def _delete_entity(self, ent):
        if self._ds:
            try:
                self._ds.delete(ent.key)
            except Exception as ex:
                logger.exception(ex)
                return False
            else:
                logger.info("Entity: {} deleted from DB".format(ent['name']))
                return True
        return False

    def get_ent_by_name(self, name):
        entity = None
        if self._ds:
            query = self._ds.query(kind=self._kind)
            query.add_filter('name', '=', name)
            try:
                entity = list(query.fetch())
            except Exception as ex:
                logger.exception(ex)
                return {}
            else:
                return entity[0] if entity and isinstance(entity, list) else {}

    def change_name_for_entity(self, ent, name):
        ent = self.get_ent_by_name(ent)
        existing_ent = self.get_ent_by_name(name)
        if existing_ent and ent:
            existing_ent['count'] += 1
            if self._delete_entity(ent):
                return self._save_entity(existing_ent)
            else:
                return False
        elif ent:
            ent['name'] = name
            return self._save_entity(ent)
        else:
            return False

    def add_or_increment_ent(self, entity):
        ent = self.get_ent_by_name(entity['name'])
        if ent:
            ent['count'] += 1
            return self._save_entity(ent)
        else:
            if self._ds:
                ent = datastore.Entity(key=self._ds.key(self._kind))
                ent['name'] = entity['name']
                ent['count'] = 1
                return self._save_entity(ent)
        return False
