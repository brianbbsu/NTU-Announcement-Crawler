from models import Session
from flask import Flask, jsonify, render_template, send_from_directory, abort
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


@app.route('/ann/<path:path>')
def ann(path):
    announcements = get_submission_list()
    announcement = next((x for x in announcements if x['digest'] == path), None)
    if not announcement:
        abort(404)
    return render_template('ann.html', ann=announcement)


@app.route('/js/<path:path>')
def js(path):
    return send_from_directory('static/javascripts', path)


@app.route('/css/<path:path>')
def css(path):
    return send_from_directory('static/stylesheets', path)


@app.route('/')
def index():
    return render_template('index.html', announcements=get_submission_list())


def run():
    app.run()


if __name__ == '__main__':
    run()
