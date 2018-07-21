from flask import Flask, request
import loader


app = Flask(__name__)

@app.route('/api/v1/')
def hello():
    return 'Running'

@app.route('/api/vi/gen', methods=['POST'])
def gen():
    post_data = request.json
    str_hash = post_data['hash']
    tensor = loader.get_pic(str_hash)
    pred_img, prediction = loader.predict(tensor)
    return

@app.route('/api/v1/model')
def mod():
    return str(loader.netG)
