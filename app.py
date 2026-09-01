from flask import Flask, g, jsonify, render_template

app = Flask(__name__)


def main():
    app.run(debug=True, port=5004)


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
