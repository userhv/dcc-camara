import sys

from Core.models.document import *
sys.path.insert(0,"..")
import psycopg2
import jwt
from Core.ports.documentRepo import *

class documentSerivce(documentRepository):
     
    def approveDocument(userName:str)->None:
        pass

  
    def createNewDocument(secretKey:str,token:str,meetingId:str,title: str,path:str,date: datetime,approved:bool)->Document:
        decoded_token = jwt.decode(
            token, secretKey, algorithms=['HS256'])
       
        if(decoded_token['user_type'] == "Chefia"):
            # create doccument already aproved
            document = documentFactory(title=title,date=date,meetingId=meetingId,path=path,approved=True)
        else:
            # create document not aproved yet
            document = documentFactory(title=title,date=date,meetingId=meetingId,path=path,approved=False)
        return document
       
    def getDocuments()->dict:
        pass
        
    def insertDB(document: Document,conn) -> str:
         
        cursor = conn.cursor()
        cursor.execute('INSERT INTO pauta (titulo, reuniao_id, documento)'
                       'VALUES (%s, %s, %s) RETURNING id',
                       (document.title, document.reunion_id, document.path))
        
        id_pauta = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return {"id_pauta": id_pauta, "reunion_id": document.meetingId}
    
