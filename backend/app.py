from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_cors import CORS
import psycopg2
import sys
import jwt
import logging
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



app.config['SECRET_KEY'] = 'ydw9iqbZby'  


@app.route('/login', methods=['POST'])
def login():
    conn = get_db_connection()
   
    data = request.get_json()
    username = data.get('nome')
   

    if not username :
        return jsonify({'message': 'Username and password are required'}), 400

    cursor = conn.cursor()
    cursor.execute("SELECT nome,role FROM usuario WHERE nome = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user is None:
        return jsonify({'message': 'User not found'}), 404


    user_id = user[0]
    user_type = user[1]
    
    token = jwt.encode({'user_id': user_id,'user_type':user_type}, app.config['SECRET_KEY'], algorithm='HS256')
  
    return jsonify({'access_token': token})


if __name__ == '__main__':
    app.run(debug=True)