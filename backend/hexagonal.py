from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'ydw9iqbZby'

from Core.adapters.userService  import *
from Core.models.user import *
from Core.adapters.meetingService import *
from Core.models.meeting import *


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
    conn = psycopg2.connect(host='localhost',
                            database='camara_db',
                            user='admin',
                            password='123456')
    meeting= meetingSerivce.createNewMeeting(title=title,date=date,token=token,secretKey=app.config['SECRET_KEY'])
    meetingId =meetingSerivce.insertDB(meeting=meeting,conn=conn)
    
    
    return jsonify({"id_reuniao": meetingId})

if __name__ == '__main__':
    app.run(debug=True)

    
