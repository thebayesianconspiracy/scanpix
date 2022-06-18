import json
import argparse
import numpy as np
from flask import Flask, jsonify, request
from media_processor import MediaProcessor
from tqdm import tqdm

INDEX_LOC = None
RESULT_LIMIT = 25
SCORE_THRESHOLD = 0.20

app = Flask(__name__)


@app.route("/")
def hello_world():
    return jsonify("scanpix ml server")


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
            result.append((index['file_name'], score))
    result = sorted(result, key=lambda x: x[1], reverse=True)
    return jsonify({'results': result[:RESULT_LIMIT], 'total_images': len(img_index)})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index-loc', type=str, help='location of the index file')
    args = parser.parse_args()

    INDEX_LOC = args.index_loc

    media_processor = MediaProcessor()
    app.run(host="0.0.0.0", port=5001, debug=True)
