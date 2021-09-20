from flask import Flask, request
from flask_restful import Api
from lib.models.db import init_db
from views import GetKeyValuePair, SetKeyValuePair, SearchKeyValuePair


app = Flask(__name__)
api = Api(app)


api.add_resource(GetKeyValuePair, '/get/<string:key>',)
api.add_resource(SetKeyValuePair, '/set',)
api.add_resource(SearchKeyValuePair, '/search',)


if __name__ == '__main__':
    init_db()
    app.run(host='172.20.0.2', port=5000, debug=True) # Reason for binding to that IP: https://stackoverflow.com/a/58138250/5378688
