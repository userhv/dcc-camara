import sys
sys.path.insert(0,"..")
from backend.Core.models.document import *
from abc import ABC, abstractmethod
class documentRepository():

    @abstractmethod
    def approveDocument(userName:str)->None:
        pass

    @abstractmethod
    def createNewDocument(secretKey:str,token:str,meetingId:str,title: str,path:str)->Document:
        pass
    
    @abstractmethod
    def getAllAgenda(token:str, secret_key:str,conn):
        pass

    @abstractmethod
    def allowed_file(filename:str,allowedExtensions:str)->str:
        pass

    @abstractmethod
    def getFileFolder(reunion_title:str, agenda_title:str, reuniao_id:str , agenda_id:str,upload_folder:str)->str:
        pass
    
    @abstractmethod
    def getBaseFolder(reunion_title:str, reunion_id:str)->str:
        pass

    @abstractmethod
    def getFile(self,reunion_title:str, agenda_title:str, reuniao_id:str, agenda_id:str, document,upload_folder:str)->str:
        pass

    @abstractmethod
    def uploadAgenda(self,reunion_title:str, agenda_title:str, reuniao_id:str, agenda_id:str, document,upload_folder:str)->None:
        pass

    @abstractmethod
    def removeAgendaFiles(self,reunion_title:str, agenda_title:str,
                    reuniao_id:str, agenda_id:str,upload_folder:str)->None:
        pass

    @abstractmethod
    def getDocuments(self,title:str,document:str,conn,reunion_id:int,upload_folder:str)->str:
        pass

    @abstractmethod
    def removeMeetingFolder(self, reuniontitles:str,agenda_titles:[],
                            reunion_id:int, agenda_ids:[])->None:
        pass

    def removeMeeting(self, reunion_id:int,upload_folder:str, conn)->None:
        pass 
    
    @abstractmethod
    def deleteDocument(self,conn,token:str,secretKey:str,document:Document,uploadFolder:str):
        pass
    @abstractmethod
    def approveDocument(token:str,secretKey:str,document:Document):
        pass
    @abstractmethod
    def getDocumentById(documentId:str)->Document:
        pass
        
    

