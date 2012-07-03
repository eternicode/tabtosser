import json

from flask import request, jsonify
from flask.views import MethodView

from . import app
from .decorators import crossdomain

pools = {
    '@pool': [],
}

class LocationAPI(MethodView):
    decorators = [crossdomain(origin='*', headers='origin, content-type')]

    def get(self, id=None):
        if id is None:
            return json.dumps(pools.keys())
        else:
            pool = pools.setdefault(id, [])[:]
            pool.extend(pools['@pool'])
            return json.dumps(pool)

    def put(self, id):
        pool = pools.setdefault(id, [])
        atpool = pools['@pool']
        if 'add' in request.form:
            url = request.form['add']
            if url in pool:
                return 'Already added', 200
            pool.append(url)
        if 'remove' in request.form:
            url = request.form['remove']
            if url not in pool+atpool:
                return 'Not present', 200
            elif url in pool:
                pool.remove(url)
            else:
                atpool.remove(url)
        return '', 204

location_api = LocationAPI.as_view('location_api')
# Seems OPTIONS is required, though the crossdomain decorator says it's not.  Need to investigate further.
app.add_url_rule('/locations/', view_func=location_api, methods=['GET', 'OPTIONS'])
app.add_url_rule('/locations/<id>', view_func=location_api, methods=['GET', 'PUT', 'OPTIONS'])
