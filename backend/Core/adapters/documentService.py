import sys
from Core.models.document import *
from backend.Core.models.document import Document
sys.path.insert(0,"..")
import psycopg2
import jwt
from Core.ports.documentRepo import *
import os
import unidecode
from werkzeug.utils import secure_filename
class documentSerivce(documentRepository):
     
    def approveDocument(userName:str)->None:
        pass
  
    def createNewDocument(secretKey:str,token:str,meetingId:str,title: str,path:str,reqUserId:str, comment:str = "")->Document:
        decoded_token = jwt.decode(
            token, secretKey, algorithms=['HS256'])
       
        if(decoded_token['user_type'] == "Chefia"):
            # create doccument already aproved
            document = documentFactory(title=title,meetingId=meetingId,approved=True,path=path,reqUserId=reqUserId, comment = comment)
        else:
            # create document not aproved yet
            document = documentFactory(title=title,meetingId=meetingId,approved=False,path=path,reqUserId=reqUserId, comment = comment)
        return document
       
    def getDocuments(self,title:str,document:str,conn,reunion_id:str,upload_folder:str)->str:

        title = unidecode.unidecode(title)
        document = unidecode.unidecode(document)
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
       
        if data:
            
            filename = self.getFile(reunion_title, agenda_title,
                            reunion_id, agenda_id,document=document, upload_folder=upload_folder)            
            return filename
            
        else:
            return 'Agenda não encontrada', 404
    
    #inserts document object in db
    def insertDB(document: Document,conn) -> str:
         
        cursor = conn.cursor()
        cursor.execute('INSERT INTO pauta (titulo,reuniao_id ,usuario_id, documento, aprovado)'
                        'VALUES (%s, %s, %s, %s,%s) RETURNING id',
                        (document.title, document.meetingId, document.reqUserId, document.path,document.approved))
        
        id_pauta = cursor.fetchone()[0]
        conn.commit()
       
        return {"id_pauta": id_pauta, "reunion_id": document.meetingId}
    
    def updateDocumentDBFile(document: Document, conn):
        cursor = conn.cursor()
        cursor.execute('UPDATE pauta SET documento = %s WHERE id = %s', (document.path, document.id))
        conn.commit()
        
    def updateDocumentDB(document:Document, conn)->str:

        cursor = conn.cursor()
        cursor.execute('UPDATE pauta SET titulo = %s, reuniao_id = %s, documento = %s, comentario = %s WHERE id = %s',
               (document.title, document.meetingId, document.path,  document.comment, document.id))

                
        id_pauta = cursor.fetchone()[0]
        conn.commit()
       
        return {"id_pauta": id_pauta, "reunion_id": document.meetingId}

    def allowed_file(filename,allowedExtensions):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowedExtensions

    def getFolder(self,reunion_title, agenda_title, reuniao_id, agenda_id,document,upload_folder):
        print(agenda_id)
        folder = reunion_title.replace("REUNIÃO DE", "").replace(
            "/", "-") + '_' + str(reuniao_id)
        folder = folder + '/' + \
            agenda_title.replace(' ', '_').lower() + "_" + str(agenda_id)
        folder = unidecode.unidecode(folder)
        path = os.path.join(upload_folder,folder.replace(" ", ""))
        return path


    def getFile(self,reunion_title, agenda_title, reuniao_id, agenda_id, document,upload_folder):

        
        path = self.getFolder(reunion_title, agenda_title, reuniao_id,
                 agenda_id,document,upload_folder).replace("REUNIAODE", "")

        return os.path.join(path, document)


    def uploadAgenda(self,reunion_title, agenda_title, reuniao_id, agenda_id, document,upload_folder):
      
        path = self.getFolder(reunion_title, agenda_title, reuniao_id, agenda_id, document,upload_folder)
    
        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, secure_filename(document.filename))
    
        document.save(file_path)  # Use a função 'save' no objeto do arquivo


    def removeAgendaFiles(self,reunion_title, agenda_title, reuniao_id, agenda_id,upload_folder,document=''):
        path = self.getFolder(reunion_title, agenda_title, reuniao_id, agenda_id,document,upload_folder)
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)

    def getAllAgenda(token:str, secret_key:str,conn):
        decoded_token = jwt.decode(
            token, secret_key, algorithms=['HS256'])
        
        user_id = decoded_token['user_id']  # Obtém o ID do usuário conectado
        cursor=conn.cursor()

        # Consulta SQL para obter os dados da agenda do usuário
        cursor.execute(''' SELECT titulo, reuniao_id, documento, aprovado, comentario, id FROM pauta ''')

        data = cursor.fetchall()
        
        # Resto do seu código para mapear e retornar os dados
        to_return = [list(i) for i in data]
        return to_return
    
    def deleteDocumentDB(self,conn,token:str,secretKey:str,document:Document,uploadFolder:str):
         
        cursor = conn.cursor()
      
        # extracting data from token
        
        
        decoded_token = jwt.decode(
            token, secretKey, algorithms=['HS256'])
     

        # only create meeting if an admin requests it
        if (decoded_token['user_type'] == "Chefia"):
            cursor.execute('''SELECT id FROM pauta
                WHERE titulo = %s''', (document.title,))
            agenda_id = cursor.fetchone()[0]
            print(agenda_id)
          
            cursor.execute('''
                DELETE FROM pauta
                WHERE reuniao_id = %s AND titulo = %s
                ''', (document.meetingId, document.title))

            conn.commit()

            cursor.execute('''
                SELECT titulo, id FROM reuniao
                WHERE id = %s
            ''', (document.meetingId,))
            data = cursor.fetchall()

            reunion_title = data[0][0]
            cursor.close()
            conn.close()

            self.removeAgendaFiles(reunion_title, document.title,document.meetingId, agenda_id,uploadFolder)

            return {"reunion_id": document.meetingId}
    
    def approveDocument(token:str,secretKey:str,document:Document)->str:
          
        decoded_token = jwt.decode(
            token, secretKey, algorithms=['HS256'])
     
        if (decoded_token['user_type'] == "Chefia"):
            document.approved=True

    def getDocumentById(documentId: str,conn) -> Document:
        cursor= conn.cursor()
        cursor.execute('''
                SELECT * FROM pauta
                WHERE id = %s
            ''', (documentId,))
        
        


    
    
    
