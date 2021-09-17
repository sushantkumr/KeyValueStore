from flask import request
from flask_restful import Resource

from lib.models import db
from lib.models.key_value_pair import KeyValuePair


class HomePage(Resource):
    def get(self):
        return {"home": "page"}


class GetKeyValuePair(Resource):
    def get(self, key):
        value = (KeyValuePair.query.filter(KeyValuePair.key == key).first()).value
        return {"value": value}


class SetKeyValuePair(Resource):
    def post(self):
        key = request.form['key']
        value = request.form['value']
        kv_object = KeyValuePair(key=key, value=value)
        db.db_session.add(kv_object)
        db.db_session.commit()
        return {key: value}


class SearchKeyValuePair(Resource):
    def get(self):
        prefix = request.args.get('prefix')
        suffix = request.args.get('suffix')
        if prefix:
            rows = KeyValuePair.query.filter(KeyValuePair.key.startswith(prefix)).all()
        elif suffix:
            rows = KeyValuePair.query.filter(KeyValuePair.key.endswith(suffix)).all()
        list_of_keys = [row.key for row in rows]
        return {'keys': list_of_keys}

