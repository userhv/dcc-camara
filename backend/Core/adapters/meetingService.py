import sys

from Core.models.meeting import *
sys.path.insert(0,"..")
import psycopg2
import jwt
from Core.ports.meetingRepo import meetingRepository

class meetingSerivce(meetingRepository):
    def getMeetingInfo(token:str,secretKey:str)->dict:
        conn = psycopg2.connect(host='localhost',
                            database='camara_db',
                            user='admin',
                            password='123456')
        cursor = conn.cursor()
        decoded_token = jwt.decode(
            token, secretKey, algorithms=['HS256'])
        data=[]
        #All meetings if a admin
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
        return {'data': data}
    
    def createNewMeeting(title:str,date:str,token,secretKey:str) -> Meeting:
        decoded_token = jwt.decode(
            token, secretKey, algorithms=['HS256'])
        # only create meeting if an admin requests it
        if(decoded_token['user_type'] == "Chefia"):
            # create meeting
            meeting = meetingFactory(title=title,date=date)
            return meeting
        else:
            Exception
    
    def insertDB(meeting: Meeting,conn) -> str:
         
        cursor = conn.cursor()
        cursor.execute('INSERT INTO reuniao (titulo, date_added)'
                        'VALUES (%s, %s) RETURNING id',
                        (meeting.title, meeting.date))
        conn.commit()
        meeting_id = cursor.fetchone()[0]
        return {"id_reuniao": meeting_id}
    