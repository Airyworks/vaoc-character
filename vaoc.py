from flask import Flask, request
from loader import get_pic


app = Flask(__name__)

@app.route('/api/v1/')
def hello():
    return 'Running'

@app.route('/api/vi/gen', methods=['POST'])
def gen():
    post_data = request.json
    str_hash = post_data['hash']

