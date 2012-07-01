import json

from flask import request, jsonify
from flask.views import MethodView

from . import app

pools = {
    '1': [],
    '2': [],
    '@pool': [],
}

class LocationAPI(MethodView):
    def get(self, id=None):
        if id is None:
            return json.dumps(pools.keys())
        else:
            if id in pools:
                return json.dumps(pools[id])
            return json.dumps(None)

    def put(self, id):
        if id in pools:
            if 'add' in request.form:
                pools[id].append(request.form['add'])
            if 'remove' in request.form:
                pools[id].remove(request.form['remove'])
        return '', 204

location_api = LocationAPI.as_view('location_api')
app.add_url_rule('/locations/', view_func=location_api, methods=['GET'])
app.add_url_rule('/locations/<id>', view_func=location_api, methods=['GET', 'PUT'])
