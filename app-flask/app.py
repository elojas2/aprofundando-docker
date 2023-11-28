from flask import Flask

app = Flask(__name__)

# @app.route('/view/<id>')
# def view_product(id):
#     return "View %s" % id

# @app.route('/buy/<id>')
# def buy_product(id):
#     return "Buy %s" % id


@app.route('/')
def tutorialspoint():
    return "ROCKET LEAGUE!"

@app.route('/teste')
def teste():
    return "Olá, mundo!"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')