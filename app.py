import os

from flask import Flask, render_template

app = Flask(__name__)


def main():
    app.run(
        host=os.environ.get('FLASK_HOST', '127.0.0.1'),
        port=int(os.environ.get('PORT', '5004')),
        debug=os.environ.get('FLASK_DEBUG', '').lower() == 'true',
    )


@app.route('/')
def index():
    response = render_template('full-dog.html')
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/frame-dog/')
def frame_dog():
    response = render_template('frame-dog.html')
    return response


if __name__ == '__main__':
    main()
