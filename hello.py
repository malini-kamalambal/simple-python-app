"""
A  simple Cloud Foundry Flask app with redis cache.

"""
import json
import os

from flask import Flask

import redis

app = Flask(__name__)


# Get Redis credentials
redis_env = dict(hostname='localhost', port=6379, password='')
if 'VCAP_SERVICES' in os.environ:
    services = json.loads(os.getenv('VCAP_SERVICES'))
    if 'rediscloud' in services:
        redis_env = services['rediscloud'][0]['credentials']
    
redis_env['host'] = redis_env['hostname']
del redis_env['hostname']
redis_env['port'] = int(redis_env['port'])


# Connect to redis
try:
    r = redis.StrictRedis(**redis_env)
    r.info()
except redis.ConnectionError:
    pass


# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))

@app.route('/')
def hello_world():
    VCAP_APPLICATION =json.loads(os.getenv("VCAP_APPLICATION"))
    instance_id = VCAP_APPLICATION['instance_index']
    application_id = VCAP_APPLICATION['application_id']
    return('Hello o/ , I am instance {0} running application {1}'.format(
        instance_id, application_id ))

@app.route('/<key>/<s>')
def add_value(key, s):
    if r:
        r.rpush(key, s)
        return 'Added {} to {}.'.format(s, key)
    else:
        abort(503)

if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)
