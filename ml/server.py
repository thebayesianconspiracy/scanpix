from flask import Flask, jsonify, request
from media_processor import MediaProcessor

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "scanpix ml server"


@app.route("/process_image")
def process_image():
    url = request.args.get('url', type=str)
    embedding = media_processor.process_image(url)
    return jsonify({"embedding": embedding})


if __name__ == '__main__':
    media_processor = MediaProcessor()
    app.run(host="0.0.0.0", port=5001, debug=True)
