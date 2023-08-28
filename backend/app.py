from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/data')
def get_data():
    data = {
        'title': 'Desenvolvimento do dcc-camara',
        'message':  'flask com angular testando'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)