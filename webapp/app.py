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

def find_dict_index_by_id(dict_list, search_id):
    return next((index for index, d in enumerate(dict_list) if d.get('originalfilepath') == search_id), -1)

def update(item, db):
    index = find_dict_index_by_id(db, item['file'])
    db[index]['name'] = item['name']
    db[index]['description'] = item['desc']
    with open(DATABASE_PATH, 'w') as f:
        json.dump(db.tolist(), f)


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
        macro = data['macro']
        origin = data['origin']

        res = db
        if macro != 'todos':
            res = res[[r['macro'] == macro for r in res]]
        if origin != 'todos':
            res = res[[r['origin'] == origin for r in res]]
        if text != '':
            res = res[[str.lower(text) in str.lower(' '.join(r['description'])) for r in res]]

        return jsonify(list(res))
    
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'GET':
        return render_template('edit.html')
    elif request.method == 'POST':

        data = request.json
        text = data['search']
        macro = data['macro']
        origin = data['origin']

        res = db
        if macro != 'todos':
            res = res[[r['macro'] == macro for r in res]]
        if origin != 'todos':
            res = res[[r['origin'] == origin for r in res]]
        if text != '':
            res = res[[str.lower(text) in str.lower(' '.join(r['description'])) for r in res]]

        return jsonify(list(res))
    
@app.route('/editItem', methods=['POST'])
def editItem():
    if request.method == 'POST':

        data = request.json
        # name = data['name']
        # desc = data['desc']
        # file = data['file']

        print(data)
        update(data, db)
        return '200'


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
