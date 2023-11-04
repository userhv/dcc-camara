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
    
    return jsonify({'data':returnDict})

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

    # download = request.args.get('download')
    conn = get_db_connection()
    documentService =documentSerivce()
    filename=documentService.getDocuments(title=title,document=document,conn=conn,reunion_id=reunion_id,upload_folder=UPLOAD_FOLDER)
    
    return send_file(filename)
        
@app.route('/new_agenda', methods=['POST'])
def postNewAgenda():
    conn =  psycopg2.connect(host='localhost',
                            database='camara_db',
                            user='admin',
                            password='123456')
   
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

    filename = secure_filename(file.filename)
    

    document = documentSerivce.createNewDocument(secretKey=app.config['SECRET_KEY'],token=token,meetingId=reunion_id,title=agenda_title,path=filename)
    document_id = documentSerivce.insertDB(document=document,conn=conn)
    cursor.execute('''SELECT titulo FROM reuniao
                      WHERE id = %s''', (reunion_id))
    reunion_title = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    dc = documentSerivce()
    dc.uploadAgenda(reunion_title, agenda_title, reunion_id, document_id, file,UPLOAD_FOLDER)
    return jsonify({"id_reuniao": reunion_id})


@app.route('/agenda', methods=['GET'])
def getAllAgendas():
    conn = get_db_connection()

    token = request.args.get('token')
    to_return = documentSerivce.getAllAgenda(token=token,secret_key=app.config["SECRET_KEY"], conn=conn)
    return jsonify({'data': to_return})

if __name__ == '__main__':
    app.run(debug=True)

    
