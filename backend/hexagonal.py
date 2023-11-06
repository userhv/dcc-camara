from flask import Flask, jsonify, render_template, request, url_for, redirect,send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'ydw9iqbZby'
from werkzeug.utils import secure_filename
from Core.adapters.userService  import *
from Core.models.user import *
from Core.adapters.meetingService import *
from Core.models.meeting import *
from Core.adapters.documentService import *
from Core.models.document import *

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

@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    username = data.get('nome')
    
    if not username:
        return jsonify({'message': 'Username and password are required'}), 400

    returnDict = userSerivce.loginUser(userName=username,secretKey=app.config['SECRET_KEY'])
    
    return jsonify(returnDict)

@app.route('/user',methods=['get'])
def getUserInfo():

    token = request.args.get('token')
    
    if not token:
        return jsonify({'message': 'Token not found'}), 400
    returnDict = userSerivce.getUserInfo(token=token,secretKey=app.config['SECRET_KEY'])

    return jsonify(returnDict)

@app.route('/meetings', methods=['get'])
def getAllMeetings():

    token = request.args.get('token')
    returnDict = meetingSerivce.getMeetingInfo(token=token,secretKey=app.config['SECRET_KEY'])
    print(returnDict['data'])
    return jsonify({'data':returnDict['data']})

@app.route('/new_meeting', methods=['POST'])
def postNewMeeting():
    
    data = request.get_json()
    token = data['token']
    date = data['date']
    title = data['title']
    conn = get_db_connection()
    meeting= meetingSerivce.createNewMeeting(title=title,date=date,token=token,secretKey=app.config['SECRET_KEY'])
    meetingId =meetingSerivce.insertDB(meeting=meeting,conn=conn)
    
    
    return jsonify({"id_reuniao": meetingId})

@app.route('/get_agenda', methods=['GET'])
def getAgenda():
    reunion_id = request.args.get('reunion_id')
    title = request.args.get('title')
    document = request.args.get('document')

    download = request.args.get('download')
    conn = get_db_connection()
    documentService =documentSerivce()
    filename=documentService.getDocuments(title,document,conn,reunion_id,UPLOAD_FOLDER)
    
    if download == 'true':
        return send_file(filename, as_attachment=True)
    return send_file(filename)
        
@app.route('/new_agenda', methods=['POST'])
def postNewAgenda():
    conn =  psycopg2.connect(host='localhost',
                            database='camara_db',
                            user='admin',
                            password='123456')
   
    cursor = conn.cursor()
  
    data = request.form
    # Usar request.form para obter os dados do formulário
    # Extracting data from form
    token = data['token']
    decoded_token = jwt.decode(
        token, app.config['SECRET_KEY'], algorithms=['HS256'])
    print("teste-------------------------------------------------------------------")
    agenda_title = data['title']
    reunion_id = data['reunion_id']

    # Verificar se um arquivo foi enviado
    if 'document' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['document']

    # Verificar se o arquivo tem um nome
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    filename = secure_filename(file.filename)

    print(decoded_token)
    
    cursor.execute('''SELECT id FROM usuario
                      WHERE nome = %s AND role = %s''', (decoded_token['user_id'], decoded_token['user_type']))
    user_id = cursor.fetchone()[0]
    document = documentSerivce.createNewDocument(secretKey=app.config['SECRET_KEY'],token=token,meetingId=reunion_id,title=agenda_title,path=filename,reqUserId=user_id)
    document_id = documentSerivce.insertDB(document=document,conn=conn)
    cursor.execute('''SELECT titulo FROM reuniao WHERE id = %s''', (reunion_id,))
    reunion_title = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    dc = documentSerivce()
    dc.uploadAgenda(reunion_title, agenda_title, reunion_id, document_id["id_pauta"], file,UPLOAD_FOLDER)
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

    ds =documentSerivce()
    document = documentFactory(meetingId=reuniao_id,title=agenda_title,path="none",approved=False,reqUserId=decoded_token['user_id'])
    to_return =ds.deleteDocumentDB(conn=conn,token=token,secretKey=app.config["SECRET_KEY"],document=document,uploadFolder=UPLOAD_FOLDER)

    return jsonify(to_return)

@app.route('/remove_meeting', methods=['POST'])
def removeMeeting():
    conn = get_db_connection()
    data = request.get_json()
    # extracting data from token
    token = data['token']
    decoded_token = jwt.decode(
        token, app.config['SECRET_KEY'], algorithms=['HS256'])
    reuniao_id = data['meeting_id']

    ds = documentSerivce()
    returnstatus = ds.removeMeeting(reuniao_id, UPLOAD_FOLDER, conn)

    return jsonify(returnstatus)

@app.route('/agenda', methods=['GET'])
def getAllAgendas():
    conn = get_db_connection()

    token = request.args.get('token')
    to_return = documentSerivce.getAllAgenda(token=token,secret_key=app.config["SECRET_KEY"], conn=conn)
    return jsonify({'data': to_return})

@app.route('/user_requests',methods=['GET'])
def getUserRequest():
    conn = get_db_connection()
    token = request.args.get('token')
    decoded_token = jwt.decode(
        token, app.config['SECRET_KEY'], algorithms=['HS256'])
    cur =conn.cursor()
    cur.execute('SELECT * FROM pauta WHERE usuario_id = %s', (decoded_token['unique_id'],))
    result = cur.fetchall()
    return jsonify({'data': result})

@app.route('/waiting_approval',methods=['GET'])
def getWaitingApproval():
    conn = get_db_connection()
    token = request.args.get('token')
    decoded_token = jwt.decode(
        token, app.config['SECRET_KEY'], algorithms=['HS256'])
    cur =conn.cursor()
    cur.execute('SELECT * FROM pauta WHERE aprovado= false', )
    result = cur.fetchall()
    return jsonify({'data':result})

@app.route('/reject_agenda', methods=['POST'])
def rejectAgenda():
    conn = get_db_connection()
    data = request.get_json()
    token = data['token']
    decoded_token = jwt.decode(
        token, app.config['SECRET_KEY'], algorithms=['HS256'])
    agendaId = data['agendaId']
    cursor =conn.cursor()
    cursor.execute('DELETE FROM pauta WHERE id = %s', (agendaId, ))
    conn.commit()
    return jsonify({'AgendaId':agendaId})


@app.route('/update_agenda_comment', methods=['POST'])
def updateAgendaComment():
    conn = get_db_connection()
    data = request.get_json()
    token = data['token']
    decoded_token = jwt.decode(
        token, app.config['SECRET_KEY'], algorithms=['HS256'])
    agendaId = data['agendaId']
    agendaComment = data['agendaComment']
    cursor =conn.cursor()
    cursor.execute('UPDATE pauta SET comentario = %s WHERE id = %s', (agendaComment, agendaId))
    conn.commit()
    return jsonify({'AgendaId':agendaId})

@app.route('/update_agenda_file', methods=['POST'])
def updateAgendaFile():
    conn =  get_db_connection()
    cursor = conn.cursor()
    data = request.form
    # Usar request.form para obter os dados do formulário
    # Extracting data from form
    token = data['token']
    decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

    print(data)
    agenda_id = data["agendaId"]
    agenda_title = data["agendaTitle"]
    meeting_id = data["meetingId"]
    
    file = request.files['document']
    filename = secure_filename(file.filename)
    print(filename)

    document = documentFactory(path=filename, id=agenda_id)
    document_id = documentSerivce.updateDocumentDBFile(document=document, conn=conn)

    cursor.execute('''SELECT titulo FROM reuniao WHERE id = %s''', (meeting_id))
    meeting_title = cursor.fetchone()[0]
    print(meeting_title)

    cursor.close()
    conn.close()

    dc = documentSerivce()
    dc.uploadAgenda(meeting_title, agenda_title, meeting_id, agenda_id, file, UPLOAD_FOLDER)

    return jsonify({"id_reuniao": meeting_id})

@app.route('/approve_agenda', methods=['POST'])
def aproveAgenda():
    conn = get_db_connection()
    data = request.get_json()
    token = data['token']
    decoded_token = jwt.decode(
        token, app.config['SECRET_KEY'], algorithms=['HS256'])
    agendaId = data['agendaId']
    cursor =conn.cursor()
    cursor.execute('UPDATE pauta SET aprovado = %s WHERE id = %s', (True, agendaId))
    conn.commit()
    return jsonify({'AgendaId':agendaId,"Approved":True})

if __name__ == '__main__':
    app.run(debug=True)

#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiRGlzY2VudGUiLCJ1c2VyX3R5cGUiOiJSZXByZXNlbnRhbnRlIERpc2NlbnRlIn0.uQV6Fi6cnMgoOdYG6_1_O6ncK-9JhqcwKxAAGPWJZKU