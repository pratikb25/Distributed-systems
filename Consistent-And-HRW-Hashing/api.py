from flask import Flask, request
from flask_restful import Resource, Api
import json, sys

app = Flask(__name__)
api = Api(app)

dictionary = {}

class Datastore(Resource):
    def get(self):
        disp = "{num_entries:" + str(len(dictionary)) + ", entries:" + str(dictionary) + "}"
        return disp, 200

    def post(self):
        json_data = request.get_json()
        for key in json_data:
            dictionary[key] = json_data[key]
        return '', 201


api.add_resource(Datastore, '/api/v1/entries')

if __name__ == '__main__':
    portnum = sys.argv[1]
    app.run(debug=True, host="127.0.0.1", port=portnum)
