"""
Flask webapp
"""

from flask import Flask, jsonify
import logging
import os
from redis import StrictRedis
import time
from .metricstore import MetricStoreFactory
from .autoscaler import Autoscaler

PORT = 8000

API_V1 = '/api/v1/'

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, static_url_path='')


REDIS = StrictRedis(host='redis', port=6379, db=0)

def scale_service(self, service_name, replica_count):
        service = self._get_service(service_name)
        service.update(mode=ServiceMode("replicated", replicas=replica_count))

# REST endpoints
@app.route(API_V1 + "health", methods=['GET'])
def health():
    """
    healthcheck endpoint
    """
    return jsonify(health=True)

@app.route(API_V1 + "count")
def index():
    """
    RESTful web service
    """
    count = REDIS.get('count')
    count = int(count) + 1 if count else 1
    REDIS.set('count', count)
    with open(args.config_file) as config_file:
        config = yaml.load(config_file)
        logger.debug("Config %s", config)
        metric_store_factory = MetricStoreFactory()
        docker_client = DockerAPIBasedClient()
        scheduler = BlockingScheduler(timezone=utc)
        autoscaler = Autoscaler(config, docker_client, metric_store_factory, scheduler)
    autoscaler.start()
    return jsonify(version='1.0', \
        count=count)

@app.errorhandler(Exception)
def handle_generic_error(err):
    """
    default exception handler
    """
    return 'error: ' + str(err), 500

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', debug=True, threaded=True, port=PORT)
    finally:
        time.sleep(15)
        logging.warn('shutting down')
