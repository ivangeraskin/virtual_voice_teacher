from flask import Flask, jsonify, request

from utils import get_model, recognize_audio
from settings import AUDIO_FRAME_RATE, N_AUDIO_CHANNELS
from settings import get_logger
logger = get_logger(logger_name=__file__)


model = get_model()
app = Flask(__name__)


@app.route("/recognize", methods=['POST'])
def recognize():
    recognized_text = recognize_audio(mp3_raw_data=request.data, model=model)
    return jsonify({
        'recognized_text': recognized_text
    })


if __name__ == '__main__':
    app.run("0.0.0.0", 8080)
