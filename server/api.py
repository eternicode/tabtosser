import json

from flask import request, jsonify
from flask.views import MethodView

from . import app


class LocationAPI(MethodView):
    def get(self, pubkey):
        if pubkey is None:
            return json.dumps([])
        else:
            return json.dumps(None)


location_api = LocationAPI.as_view('location_api')
app.add_url_rule('/locations/', defaults={'pubkey': None},
                view_func=location_api, methods=['GET',])
app.add_url_rule('/locations/', view_func=location_api, methods=['POST',])
app.add_url_rule('/locations/<pubkey>', view_func=location_api,
                methods=['GET', 'PUT', 'DELETE'])
