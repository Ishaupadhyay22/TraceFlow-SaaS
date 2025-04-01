import requests


class PrometheusMetricStore(object):
    def __init__(self, config):
        self.config = config

    def get_metric_value(self, metric_query):
        prometheus_url = self.config['url']
        prometheus_query_url1 = "{}/api/v1/rest-count".format(prometheus_url)
        prometheus_query_url2 = "{}/api/v1/rest-ip".format(prometheus_url)
        resposnse = requests.get(prometheus_query_url, params=dict(query=metric_query))
        resposnse_json = resposnse.json()
        return float(resposnse_json['data']['result'][1])