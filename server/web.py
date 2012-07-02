import re
from tempfile import mkstemp
from os import unlink, fdopen

from yuicompressor import run as yuic

from flask import request, render_template
from flask.views import MethodView

from . import app


class IndexView(MethodView):
    def get(self):
        loc = request.args.get('location', 1)

        # Tempfiles
        bm1fd, bm1 = mkstemp('.js')
        bm2fd, bm2 = mkstemp('.js')

        # Render from template js
        bm = render_template(
            'bookmarklet.js',
            host=request.host_url,
            location=loc
        )
        bm1f = fdopen(bm1fd, 'w')
        bm1f.write(bm)
        bm1f.close()

        # Compress
        yuic(bm1, '-o', bm2)

        # Read from outfile (yuicompressor has no proper API)
        bm2f = fdopen(bm2fd, 'r')
        bm = bm2f.read()
        bm2f.close()

        # Delete tempfiles
        unlink(bm1)
        unlink(bm2)

        return render_template('index.html', bookmarklet=bm)

index_view = IndexView.as_view('index_view')
app.add_url_rule('/', view_func=index_view, methods=['GET'])

def script():
    """
    For debugging.  From a console (Chrome inspector, Firebug, etc):
    s = document.createElement('script'); s.src= 'http://127.0.0.1:5000/script.js?location=<currloc>'; document.head.appendChild(s);

    Script will run as if automatically invoked (eg, browser may suppress new pages as popups)
    """
    loc = request.args.get('location', 1)
    bm = render_template(
        'bookmarklet.js',
        host=request.host_url,
        location=loc
    )
    return bm

app.add_url_rule('/script.js', view_func=script, methods=['GET'])
