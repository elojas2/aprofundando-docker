from flask import Flask, Response, request
from prometheus_client import Counter, Gauge, generate_latest
import random

app = Flask(__name__)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

def random_number():
    return str(random.choice([200, 300, 500]))

numero_requests = Counter(
    'app_flask_numero_requests',
    'o numero de requests, contador.',
    ['status_code']
)

requests = Gauge(
    'requests',
    'A memoria que esta sendo usada (aleatoriamente).',
    ['server_name', 'location']
)

# metrica do anyeon
location_requests = Counter(
    'location_requests',
    'Number of requests for each location.',
    ['status_code']
)

#pagina principal com algumas metricas
@app.route('/start')
def start():
    valor = random_number()
    numero_requests.labels(valor).inc()
    requests.labels('server-a', 'principal').set(random.randint(10000, 90000))

    return "principal"

#pagina anyeon com algumas metricas
@app.route('/anyeon')
def anyeon():
    location_requests.labels(random_number()).inc()
    requests.labels('server-a', 'anyeon').set(random.randint(10000, 90000))
    return 'anyeon'


@app.route('/metrics', methods=['GET'])
def get_data():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
