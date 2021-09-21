from flask import request
from flask_restful import Resource
from prometheus_flask_exporter import RESTfulPrometheusMetrics

from lib.models import db
from lib.models.key_value_pair import KeyValuePair


metrics = RESTfulPrometheusMetrics.for_app_factory()


class GetKeyValuePair(Resource):
    def get(self, key):
        row = (KeyValuePair.query.filter(KeyValuePair.key == key).first())
        if row:
            value = row.value
            return {"value": value}
        else:
            return {"message": "Key value pair does not exist"}


class SetKeyValuePair(Resource):
    def post(self):
        key = request.form['key']
        value = request.form['value']
        row = (KeyValuePair.query.filter(KeyValuePair.key == key).first())
        if row:
            row.value = value
        else:
            row = KeyValuePair(key=key, value=value)
        db.db_session.add(row)
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

