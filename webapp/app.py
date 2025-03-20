import json
import base64
import numpy as np
from os import path, getenv
from flask import Flask, jsonify, request, render_template, send_from_directory
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from dotenv import load_dotenv

DATABASE_PATH = path.join('..', 'data', 'database.json')

load_dotenv()

app = Flask(__name__, static_url_path='/static')

# env_config = getenv("APP_SETTINGS", "config.DevelopmentConfig")
# app.config.from_object(env_config)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# from models import Macro, Submacro, Micro, TimestampMixin


# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)


if __name__ == '__main__':
    app.run()


with open(DATABASE_PATH, 'r') as f:
    db = json.load(f)
    db = np.array(db)


@app.route('/image/<path:path>')
def send_image(path):
    return send_from_directory('images', path)

@app.route('/thumb/<path:path>')
def send_thumb(path):
    return send_from_directory('thumbs', path)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':

        data = request.json
        text = data['search']

        res = []
        if text == '':
            res = db
        else:
            # TODO: better search function
            res = db[[str.lower(text) in str.lower(
                ' '.join(d['ocr'])) for d in db]]

        for r in res:
            with open(path.join('thumbs', r['originalfilepath']), 'rb') as f:
                thumb = f.read()
                r['thumb_data'] = str(base64.b64encode(thumb))

        return jsonify(list(res))


@app.route('/table', methods=['GET', 'POST'])
def table():
    if request.method == 'GET':
        return render_template('table.html', data=db[:100])
    elif request.method == 'POST':

        data = request.json
        text = data['search']

        res = []
        if text != '':
            # TODO: better search function
            res = db[[str.lower(text) in str.lower(
                ' '.join(d['description'])) for d in db]]

            # for r in res:
            #     with open(path.join('thumbs', r['file']), 'rb') as f:
            #         thumb = f.read()
            #         r['thumb_data'] = str(base64.b64encode(thumb))

        return jsonify(list(res))
