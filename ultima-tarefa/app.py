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

memoria_usada = Gauge(
    'memoria_usada',
    'A memoria que esta sendo usada (aleatoriamente).',
    ['server_name', 'location']
)

# Metrics specific to locations
location_requests = Counter(
    'location_requests',
    'Number of requests for each location.',
    ['status_code']
)

# location_response_time = Gauge(
#     'location_response_time',
#     'Response time for each location.',
#     ['location']
# )

@app.route('/start')
def start():
    valor = random_number()
    numero_requests.labels(valor).inc()
    memoria_usada.labels('server-a', 'principal').set(random.randint(10000, 90000))

    return "princiapl"

@app.route('/anyeon')
def anyeon():
    location_requests.labels(random_number()).inc()
    memoria_usada.labels('server-a', 'anyeon')
    return 'anyeon'


@app.route('/metrics', methods=['GET'])
def get_data():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
