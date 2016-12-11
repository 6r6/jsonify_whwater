from flask import Flask, Response, jsonify
from Monitor import output

app = Flask(__name__)


@app.route('/whwater/v1')
@app.route('/whwater/v1/')
def hello_world():
    if output():
        response = Response(output(),
                            content_type="application/json; charset=utf-8"), 201
        return response
    else:
        return jsonify({'status': 'error'})


if __name__ == '__main__':
    app.run()
