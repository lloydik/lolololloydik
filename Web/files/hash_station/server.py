from flask import Flask, request, render_template
import hashlib

app = Flask(__name__)
flag = open('flag.txt').read()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hash/')
def get_hash():
    data = request.args.get('data', '') + flag
    result = ''
    for i in range(0, len(data), 8):
        block = hashlib.md5(data[i: i + 8].encode()).hexdigest() + "\n"
        result += block
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)