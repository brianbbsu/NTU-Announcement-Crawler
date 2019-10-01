from models import Session
from flask import Flask, jsonify, send_from_directory
from utils import get_submission_list


app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()


@app.route('/api/check')
def check():
    return "Ok."


@app.route('/api/')
def api_main():
    return jsonify(get_submission_list())


@app.route('/<path:path>')
def server(path):
    return send_from_directory('public', path)


@app.route('/')
def index():
    return send_from_directory('public', 'index.html')


def run():
    app.run()


if __name__ == '__main__':
    run()
