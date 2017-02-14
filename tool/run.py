from gevent import monkey
monkey.patch_all()

from gevent.wsgi import WSGIServer
from web import app

http_server = WSGIServer(('', 80), app)
http_server.serve_forever()

# app.run(host='0.0.0.0', port=8080, debug=True, threaded=False)
