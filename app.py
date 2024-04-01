from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World! This is my API.'

@app.route('/api/data')
def get_data():
    return {'data': 'example'}

if __name__ == '__main__':
    app.run()