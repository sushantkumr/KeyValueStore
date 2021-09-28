from flask import request, Response
from flask_restful import Resource
from prometheus_client import Counter, generate_latest

from lib.models import db
from lib.models.key_value_pair import KeyValuePair


CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

get_counter = Counter(
    'get_counter',
    'Counts the number of get requests'
)

set_counter = Counter(
    'set_counter',
    'Counts the number of set requests'
)

search_counter = Counter(
    'search_counter',
    'Counts the number of search requests'
)

class GetKeyValuePair(Resource):
    def get(self, key):
        get_counter.inc()
        row = (KeyValuePair.query.filter(KeyValuePair.key == key).first())
        if row:
            value = row.value
            return {"value": value}
        else:
            return {"message": "Key value pair does not exist"}


class SetKeyValuePair(Resource):
    def post(self):
        set_counter.inc()
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
        search_counter.inc()
        prefix = request.args.get('prefix')
        suffix = request.args.get('suffix')
        if prefix:
            rows = KeyValuePair.query.filter(KeyValuePair.key.startswith(prefix)).all()
        elif suffix:
            rows = KeyValuePair.query.filter(KeyValuePair.key.endswith(suffix)).all()
        list_of_keys = [row.key for row in rows]
        return {'keys': list_of_keys}


class Metrics(Resource):
    def get(self):
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
