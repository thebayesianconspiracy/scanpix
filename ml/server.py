import os
import json
import argparse
import numpy as np
import sqlite3
import random
from tqdm import tqdm
from datetime import datetime
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_socketio import SocketIO, send, emit
from media_processor import MediaProcessor

INDEX_LOC = None
IMG_LOC = None
IMG_INDEX = None
LOAD_TOGGLE_ON_COMPLETE_INDEXING = True
RESULT_LIMIT = 100
SCORE_THRESHOLD = 0.20
TEMPLATE_DIR = os.path.abspath('app')
STATIC_FOLDER = os.path.abspath('app')
MODE = os.getenv('MODE', "local")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_FOLDER, static_url_path='')
socket = SocketIO(app)


@app.route("/")
def hello_world():
    return render_template('index.html', loc=INDEX_LOC, imgs=len(IMG_INDEX), mode=MODE)


@app.route("/image/<path:name>")
def serve_image(name):
    return send_from_directory(IMG_LOC, name)


@app.route("/process_image")
def process_image():
    url = request.args.get('url', type=str)
    print(url)
    return jsonify(media_processor.process_image(url))


@app.route("/process_text")
def process_text():
    text = request.args.get('text', type=str)
    return jsonify(media_processor.process_text(text))


@app.route("/search")
def search():
    assert IMG_INDEX
    text = request.args.get('text', type=str)
    if text == "":
        result_count = len(IMG_INDEX)
        result = [(index['file_name'], i) for i, index in enumerate(IMG_INDEX)]
        random.shuffle(result)
        result = result[:RESULT_LIMIT]
        row_id = -1
    else:
        embedding = media_processor.process_text(text)['clip_embedding']
        result = []
        for index in tqdm(IMG_INDEX):
            score = np.dot(embedding, index['clip_embedding'])
            if score > SCORE_THRESHOLD:
                result.append((index['file_name'], score))
        result_count = len(result)
        result = sorted(result, key=lambda x: x[1], reverse=True)[:RESULT_LIMIT]

        with sqlite3.connect(os.path.join(INDEX_LOC, 'scanpix.db')) as connection:
            cur = connection.cursor()
            cur.execute("insert into queries values (?, ?, ?, ?)", (datetime.now(), text, result_count, 0))
            connection.commit()
            row_id = cur.lastrowid

    return jsonify({'results': result, 'total_images': len(IMG_INDEX), 'result_count': result_count, 'row_id': row_id})


@app.route("/feedback", methods=['POST'])
def feedback():
    feedback = 1 if request.json['feedback'] == 'positive' else -1 if request.json['feedback'] == 'negative' else 0
    if request.json['row_id'] >= 0:
        with sqlite3.connect(os.path.join(INDEX_LOC, 'scanpix.db')) as connection:
            cur = connection.cursor()
            cur.execute(f"update queries set feedback={feedback} where rowid={request.json['row_id']}")
            connection.commit()
    return jsonify({"message": "success"})


@socket.on("indexer_progress_event")
def handle_indexer_progress_event(data):
    global LOAD_TOGGLE_ON_COMPLETE_INDEXING
    app.logger.info(f"progress => {data}")
    emit("send_progress_to_frontend", data, broadcast=True)
    ratio = int(data.split('_')[0]) // int(data.split('_')[1])
    reload_json(ratio)


# ensures index is loaded only once everytime it first reaches 100%
def reload_json(ratio):
    global LOAD_TOGGLE_ON_COMPLETE_INDEXING
    if ratio == 1:
        if LOAD_TOGGLE_ON_COMPLETE_INDEXING:
            app.logger.info("Indexing Complete, reloading JSON!")
            load_index_json()
            LOAD_TOGGLE_ON_COMPLETE_INDEXING = False
    else:
        LOAD_TOGGLE_ON_COMPLETE_INDEXING = True


def load_index_json():
    global IMG_INDEX
    with open(f'{INDEX_LOC}/index.json', 'r') as fob:
        IMG_INDEX = json.load(fob)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index-loc', type=str, help='location of the index file', default="../data/")
    args = parser.parse_args()

    INDEX_LOC = os.path.abspath(os.path.join(args.index_loc, "db"))
    IMG_LOC = os.path.abspath(os.path.join(args.index_loc, "images"))

    with sqlite3.connect(os.path.join(INDEX_LOC, 'scanpix.db')) as connection:
        cur = connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS queries (ts timestamp, query text, results int, feedback int)")
        connection.commit()

    load_index_json()
    media_processor = MediaProcessor()
    socket.run(app, host="0.0.0.0", port=5001, debug=True)
