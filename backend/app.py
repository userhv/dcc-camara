from flask import Flask, jsonify, render_template, request, url_for, redirect, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import psycopg2
import sys
import jwt
import logging
import json
import os
import unidecode
app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='camara_db',
                            user='admin',
                            password='123456')
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def getFolder(reunion_title, agenda_title, reuniao_id, agenda_id,):
    folder = reunion_title.replace("REUNIÃO DE", "").replace(
        "/", "-") + '_' + str(reuniao_id)
    folder = folder + '/' + \
        agenda_title.replace(' ', '_').lower() + "_" + str(agenda_id)
    folder = unidecode.unidecode(folder)
    path = os.path.join(app.config['UPLOAD_FOLDER'], folder.replace(" ", ""))
    return path


def getFile(reunion_title, agenda_title, reuniao_id, agenda_id, document):
    path = getFolder(reunion_title, agenda_title, reuniao_id,
                     agenda_id).replace("REUNIAODE", "")

    print(path)
    print(document)

    print(os.path.join(path, document))

    return os.path.join(path, document)


def uploadAgenda(reunion_title, agenda_title, reuniao_id, agenda_id, document):
    path = getFolder(reunion_title, agenda_title, reuniao_id, agenda_id)

    if not os.path.exists(path):
        os.makedirs(path)

    file_path = os.path.join(path, secure_filename(document.filename))
    document.save(file_path)  # Use a função 'save' no objeto do arquivo


def removeAgendaFiles(reunion_title, agenda_title, reuniao_id, agenda_id):
    path = getFolder(reunion_title, agenda_title, reuniao_id, agenda_id)
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)

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

    token = jwt.encode({'user_id': user_id, 'user_type': user_type}, app.config['SECRET_KEY'], algorithm='HS256')

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

@app.route('/get_agenda', methods=['GET'])
def getAgenda():
    reunion_id = request.args.get('reunion_id')
    title = request.args.get('title')
    document = request.args.get('document')

    download = request.args.get('download')

    print(download)

    title = unidecode.unidecode(title)
    document = unidecode.unidecode(document)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT titulo FROM reuniao
                      WHERE id = %s''', (reunion_id))
    reunion_title = cursor.fetchall()[0][0]

    reunion_title = unidecode.unidecode(reunion_title)
    cursor.execute(
        'SELECT id, titulo FROM pauta WHERE reuniao_id = %s AND documento = %s', (reunion_id, document))
    data = cursor.fetchall()
    agenda_id = data[0][0]
    agenda_title = data[0][1]
    cursor.close()
    conn.close()


    if data:
        filename = getFile(reunion_title, agenda_title,
                           reunion_id, agenda_id, document)
        
        if download == "true":
            print("IOUAGUDIGAUDGASUDAP")
            return send_file(filename, as_attachment=True)
        return send_file(filename)
        
    else:
        return 'Agenda não encontrada', 404

@app.route('/new_agenda', methods=['POST'])
def postNewAgenda():
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.form  # Usar request.form para obter os dados do formulário

    # Extracting data from form
    token = data['token']
    decoded_token = jwt.decode(
        token, app.config['SECRET_KEY'], algorithms=['HS256'])
    agenda_title = data['title']
    reunion_id = data['reunion_id']

    # Verificar se um arquivo foi enviado
    if 'document' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['document']

    # Verificar se o arquivo tem um nome
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Verificar se a extensão do arquivo é permitida
    if not allowed_file(file.filename):
        return jsonify({'message': 'File extension not allowed'}), 400

    # Salvar o arquivo no servidor
    filename = secure_filename(file.filename)

    # Agora você pode continuar com a criação da pauta no banco de dados

    cursor.execute('INSERT INTO pauta (titulo, reuniao_id, documento)'
                   'VALUES (%s, %s, %s) RETURNING id, titulo, documento',
                   (agenda_title, reunion_id, filename))
    data = cursor.fetchall()

    agenda_id = data[0][0]

    conn.commit()

    cursor.execute('''SELECT titulo FROM reuniao
                      WHERE id = %s''', (reunion_id))
    reunion_title = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    uploadAgenda(reunion_title, agenda_title, reunion_id, agenda_id, file)
    return jsonify({"id_reuniao": reunion_id})

@app.route('/remove_agenda', methods=['POST'])
def removeAgenda():
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    # extracting data from token
    token = data['token']
    decoded_token = jwt.decode(
        token, app.config['SECRET_KEY'], algorithms=['HS256'])
    reuniao_id = data['reuniaoId']
    agenda_title = data['title']

    # only create meeting if an admin requests it
    if (decoded_token['user_type'] == "Chefia"):
        cursor.execute('''SELECT id FROM pauta
            WHERE titulo = %s''', (agenda_title,))
        agenda_id = cursor.fetchone()[0]
        print(agenda_id)
        # delete meeting
        cursor.execute('''
            DELETE FROM pauta
            WHERE reuniao_id = %s AND titulo = %s
            ''', (reuniao_id, agenda_title))

        conn.commit()

        cursor.execute('''
            SELECT titulo, id FROM reuniao
            WHERE id = %s
        ''', (reuniao_id,))
        data = cursor.fetchall()

        reunion_title = data[0][0]
        cursor.close()
        conn.close()

        removeAgendaFiles(reunion_title, agenda_title, reuniao_id, agenda_id)

        return jsonify({"reunion_id": reuniao_id})

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
        cursor.execute("SELECT * FROM reuniao ORDER BY date_added, id")
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
        cursor.execute('''SELECT * from reuniao WHERE id in %s
                          ORDER BY date_added, id''', (tuple(all_meetings),))
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