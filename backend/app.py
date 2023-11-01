from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_cors import CORS
import psycopg2
import sys
import jwt
import logging
import json
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
    print(request)
    print(data)

    if not username:
        return jsonify({'message': 'Username and password are required'}), 400

    cursor = conn.cursor()
    cursor.execute(
        "SELECT nome,role FROM usuario WHERE nome = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    user_id = user[0]
    user_type = user[1]

    token = jwt.encode({'user_id': user_id, 'user_type': user_type}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    return jsonify({'access_token': token, "user":user_id, "user_type":user_type})

@app.route('/user',methods=['get'])
def getUserInfo():
    conn = get_db_connection()
    cursor = conn.cursor()
    token = request.args.get('token')

    decoded_token = jwt.decode( token, app.config['SECRET_KEY'], algorithms=['HS256'])
    print(decoded_token)
    return jsonify({'username':decoded_token['user_id'],'role':decoded_token['user_type']})

@app.route('/agenda', methods=['GET'])
def getAllAgendas():
    conn = get_db_connection()
    cursor = conn.cursor()
    token = request.args.get('token')
    decoded_token = jwt.decode(
        token, app.config['SECRET_KEY'], algorithms=['HS256'])
    
    user_id = decoded_token['user_id']  # Obtém o ID do usuário conectado

    # Consulta SQL para obter os dados da agenda do usuário
    if(decoded_token['user_type'] == "Chefia"):
        cursor.execute('''
            SELECT titulo, reuniao_id, documento
            FROM pauta
        ''')
    else:
        cursor.execute('''
            SELECT titulo, reuniao_id, documento
            FROM pauta
            WHERE reuniao_id IN (
                SELECT reuniao_id
                FROM usuario_reuniao
                WHERE usuario_id IN (
                    SELECT ID 
                    FROM usuario
                    WHERE nome = %s
                )
            )
        ''', (user_id,))
    
    data = cursor.fetchall()
    
    # Resto do seu código para mapear e retornar os dados
    to_return = [list(i) for i in data]
    print(to_return)
    
    return jsonify({'data': to_return})

@app.route('/meetings', methods=['get'])
def getAllMeetings():
    conn = get_db_connection()
    cursor = conn.cursor()
    token = request.args.get('token')

    decoded_token = jwt.decode(
        token, app.config['SECRET_KEY'], algorithms=['HS256'])
   
    data=[]
    #All meeting if a admin
    if(decoded_token['user_type'] == "Chefia"):
        cursor.execute("SELECT * FROM reuniao")
        data = cursor.fetchall()
    #only fetch meetings a normal user is in
    if(decoded_token['user_type'] == "Representante Discente"):
       
        # this whole thing probably better with joins
        # Get user id from user name
        cursor.execute(
            "SELECT  ID FROM usuario WHERE nome = %s", (decoded_token['user_id'],))
        user_id = cursor.fetchone()[0]
        
        # Get all meetings ids that user have access too
        cursor.execute(
            'SELECT reuniao_id from usuario_reuniao WHERE usuario_id =%s', (user_id,))
        all_meetings = cursor.fetchall()
        all_meetings= [i[0] for i in all_meetings] 
        # Get full info from meetings from meetings ids
        cursor.execute('SELECT * from reuniao WHERE id in %s', (tuple(all_meetings),))
        data= cursor.fetchall()

    #Now that we have the meetings we need to get the participants of those meetings
    to_return = [list(i) for i in data]
    for index,i in enumerate(data):
            reuniao_id =i[0]
            cursor.execute("SELECT usuario_id FROM usuario_reuniao WHERE reuniao_id=%s",(reuniao_id,))
            users = cursor.fetchall()
            users= [user[0] for user in users] 
            if len(users)>0:
                cursor.execute("SELECT nome FROM usuario WHERE id IN %s", (tuple(users),))
                names = cursor.fetchall()
                to_return[index].append(names)
    return jsonify({'data': to_return})

@app.route('/new_meeting', methods=['POST'])
def postNewMeeting():
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    # extracting data from token
    token = data['token']
    decoded_token = jwt.decode(
        token, app.config['SECRET_KEY'], algorithms=['HS256'])
    date = data['date']
    title = data['title']

    participants = ["Discente", "eu", "Chefe"]

    # only create meeting if an admin requests it
    if(decoded_token['user_type'] == "Chefia"):
        # create meeting
        cursor.execute('INSERT INTO reuniao (titulo, date_added)'
                       'VALUES (%s, %s) RETURNING id',
                       (title, date))
        meeting_id = cursor.fetchone()[0]

        # for each participant, create meeting x user relationship in the  correct tablp
        for i in participants:
            cursor.execute("SELECT id FROM usuario WHERE nome = %s", (i,))
            user_id = cursor.fetchone()[0]
            cursor.execute('INSERT INTO usuario_reuniao(usuario_id , reuniao_id)'
                           'VALUES (%s,%s)', (user_id, meeting_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"id_reuniao": meeting_id})


if __name__ == '__main__':
    app.run(debug=True)

    #
#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiRGlzY2VudGUiLCJ1c2VyX3R5cGUiOiJSZXByZXNlbnRhbnRlIERpc2NlbnRlIn0.uQV6Fi6cnMgoOdYG6_1_O6ncK-9JhqcwKxAAGPWJZKU