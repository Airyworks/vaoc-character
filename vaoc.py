from flask import Flask, request
import loader
import random
import base64

mapping = {}
pool = [i + 1 for i in range(10)]
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
    byte_img = pred_img.tobytes()
    return base64.b64encode(byte_img).decode('utf-8')

@app.route('/api/v1/model')
def mod():
    return str(loader.netG)

@app.route('/api/v1/fakegen', methods=['POST'])
def fgen():
    post_data = request.json
    str_hash = post_data['hash']
    if str_hash in mapping.keys():
        name = str(mapping[str_hash])
    else:
        if len(pool) == 0:
            pool = [i + 1 for i in range(10)]
        name = random.choice(pool)
        pool.remove(name)
    path = f'./release/{name}.png'
    with open(path, 'rb') as f_obj:
        b = f_obj.read()

    c = base64.b64encode(b)
    return c.decode('utf-8')

if __name__ == '__main__':
    app.run('0.0.0.0')
