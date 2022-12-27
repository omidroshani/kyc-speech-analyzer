import flask
from flask import jsonify
from flask import request
import json
import uuid
from flask import current_app as app, send_file, abort
import os
import uuid
import requests
from pathlib import Path
from voice_extractor import VoiceAnalsis
from random_text import TextGenerator

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/speech/url/', methods=['POST'])
def get_voice_by_url():
    url = request.form.get('url')
    text = request.form.get('text')

    Path("tmp").mkdir(exist_ok=True)
    
    r = requests.get(url)
    tmp_file_path = f'tmp/{str(uuid.uuid4())}.wav'

    with open(tmp_file_path, 'wb') as f :
        f.write(r.content)


    a = VoiceAnalsis(tmp_file_path)
    return jsonify({'status':'successful','conf':a.is_match_with_text(text),'filename':tmp_file_path.replace('tmp/','')})


@app.route('/random-text', methods=['GET'])
def get_random_text():
    type = request.args.get('type', 'sentence')
    count = int(request.args.get('count', 1))
    
    a = TextGenerator()
    if type == 'vocab':
        data = a.random_vocab(count=count)
    else:
        data = a.random_sentence(count)
    return jsonify({'status':'successful','result':data})

@app.route('/speech/file/', methods=['POST'])
def ocr_by_file():

    uploaded_file = flask.request.files.get('file')
    text = request.form.get('text')
    
    Path("tmp").mkdir(exist_ok=True)

    tmp_file_path = f'tmp/{str(uuid.uuid4())}.wav'
    uploaded_file.save(tmp_file_path)

    a = VoiceAnalsis(tmp_file_path)
    return jsonify({'status':'successful','conf':a.is_match_with_text(text),'filename':tmp_file_path.replace('tmp/','')})




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT',7000)))
