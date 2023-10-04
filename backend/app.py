from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='camara_db',
                            user='admin',
                            password='123456')
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM usuario;')
    usuario = cur.fetchall()
    cur.close()
    conn.close()
    data = {
        'nome': usuario[0][1],
        'cargo': usuario[0][2],

    }
    return jsonify(data)
    # return render_template('index.html', usuario=usuario)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        role = request.form['role']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO usuario (nome, role)'
                    'VALUES (%s, %s)',
                    (nome, role))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)