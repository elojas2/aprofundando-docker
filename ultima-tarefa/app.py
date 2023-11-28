from flask import Flask, Response
from prometheus_client import Counter, Gauge, generate_latest
import random

app = Flask(__name__)

CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

numero_requests = Counter(
    'app_flask_numero_requests',
    'o numero de requests, contador.',
    ['status_code']
)

memoria_usada = Gauge(
    'memoria_usada',
    'A memoria que esta sendo usada (aleatoriamente).',
    ['server_name']
)
@app.route('/')
def start():
    return "hello"


@app.route('/metrics', methods=['GET'])
def get_data():
    #random status code
    random_status_code = str(random.choice([200,300,500]))

    numero_requests.labels(random_status_code).inc()
    memoria_usada.labels('server-a').set(random.randint(10000,90000))
    
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0')