from models import Session, Announcement
from flask import Flask, jsonify, render_template, send_from_directory, abort
from utils import get_submission_list
import config


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
    session = Session()
    announcements = session.query(Announcement).filter_by(present=True, digest=path).all()
    if not announcements:
        abort(404)
    if len(announcements) > 1:
        abort(500)
    return render_template('ann.html', announcement=announcements[0])


@app.route('/')
def index():    
    return render_template('index.html', announcements=get_submission_list())


def run():
    app.run(host=config.get('host'), port=config.get('port'))


if __name__ == '__main__':
    run()
