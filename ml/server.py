import os
import json
import argparse
import numpy as np
from tqdm import tqdm
import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request, render_template, send_from_directory
from media_processor import MediaProcessor

INDEX_LOC = None
IMG_LOC = None
RESULT_LIMIT = 25
SCORE_THRESHOLD = 0.20
TEMPLATE_DIR = os.path.abspath('app')
STATIC_FOLDER = os.path.abspath('app')
MODE = os.getenv('MODE', "local")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_FOLDER, static_url_path='')


@app.route("/")
def hello_world():
    with open(f'{INDEX_LOC}/index.json', 'r') as fob:
        img_index = json.load(fob)
    return render_template('index.html', loc=INDEX_LOC, imgs=len(img_index), mode=MODE)


@app.route("/image/<path:name>")
def serve_image(name):
    return send_from_directory(IMG_LOC, name)


@app.route("/process_image")
def process_image():
    url = request.args.get('url', type=str)
    return jsonify(media_processor.process_image(url))


@app.route("/process_text")
def process_text():
    text = request.args.get('text', type=str)
    return jsonify(media_processor.process_text(text))


@app.route("/search")
def search():
    with open(f'{INDEX_LOC}/index.json', 'r') as fob:
        img_index = json.load(fob)
    text = request.args.get('text', type=str)
    if text == "":
        img_index.reverse()
        result = [(index['file_name'], index['file_location'], i) for i, index in enumerate(img_index)][:RESULT_LIMIT]
        row_id = -1
    else:
        embedding = media_processor.process_text(text)['clip_embedding']
        result = []
        for index in tqdm(img_index):
            score = np.dot(embedding, index['clip_embedding'])
            if score > SCORE_THRESHOLD:
                result.append((index['file_name'], index['file_location'], score))
        result = sorted(result, key=lambda x: x[2], reverse=True)[:RESULT_LIMIT]

        with sqlite3.connect(os.path.join(INDEX_LOC, 'scanpix.db')) as connection:
            cur = connection.cursor()
            cur.execute("insert into queries values (?, ?, ?, ?)", (datetime.now(), text, len(result), 0))
            connection.commit()
            row_id = cur.lastrowid

    return jsonify({'results': result, 'total_images': len(img_index), 'row_id': row_id})


@app.route("/feedback", methods=['POST'])
def feedback():
    feedback = 1 if request.json['feedback'] == 'positive' else -1 if request.json['feedback'] == 'negative' else 0
    if request.json['row_id'] >= 0:
        with sqlite3.connect(os.path.join(INDEX_LOC, 'scanpix.db')) as connection:
            cur = connection.cursor()
            cur.execute(f"update queries set feedback={feedback} where rowid={request.json['row_id']}")
            connection.commit()
    return jsonify({"message": "success"})


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

    media_processor = MediaProcessor()
    app.run(host="0.0.0.0", port=5001, debug=True)
