import os
import json
import argparse
import numpy as np
from flask import Flask, jsonify, request, render_template, send_from_directory
from media_processor import MediaProcessor
from tqdm import tqdm


INDEX_LOC = None
IMG_LOC = None
RESULT_LIMIT = 25
SCORE_THRESHOLD = 0.20
TEMPLATE_DIR = os.path.abspath('../app')
STATIC_FOLDER = os.path.abspath('../app')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_FOLDER, static_url_path='')


@app.route("/")
def hello_world():
    with open(f'{INDEX_LOC}/index.json', 'r') as fob:
        img_index = json.load(fob)
    return render_template('index.html', loc=INDEX_LOC, imgs=len(img_index))


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
    embedding = media_processor.process_text(text)['clip_embedding']
    result = []
    for index in tqdm(img_index):
        score = np.dot(embedding, index['clip_embedding'])
        if score > SCORE_THRESHOLD:
            result.append((index['file_name'], index['file_location'], score))
    result = sorted(result, key=lambda x: x[2], reverse=True)
    return jsonify({'results': result[:RESULT_LIMIT], 'total_images': len(img_index)})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index-loc', type=str, help='location of the index file', default="../data/")
    args = parser.parse_args()

    INDEX_LOC = os.path.abspath(args.index_loc)
    IMG_LOC = os.path.abspath(os.path.join(args.index_loc, "images"))

    media_processor = MediaProcessor()
    app.run(host="0.0.0.0", port=5001, debug=True)
