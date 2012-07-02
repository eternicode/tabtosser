import json

from flask import request, jsonify
from flask.views import MethodView

from . import app
from .decorators import crossdomain

pools = {
    '1': [],
    '2': [],
    '@pool': [],
}

class LocationAPI(MethodView):
    decorators = [crossdomain(origin='*')]

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
# Seems OPTIONS is required, though the crossdomain decorator says it's not.  Need to investigate further.
app.add_url_rule('/locations/', view_func=location_api, methods=['GET', 'OPTIONS'])
app.add_url_rule('/locations/<id>', view_func=location_api, methods=['GET', 'PUT', 'OPTIONS'])
