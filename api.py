from models import Session
from flask import Flask, jsonify
from utils import get_submission_list

app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

@app.route('/check')
def check():
    return "Ok."

@app.route('/')
def index():
    return jsonify(get_submission_list())

def run():
    app.run()

if __name__ == '__main__':
    run()
