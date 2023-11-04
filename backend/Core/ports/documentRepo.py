import sys
sys.path.insert(0,"..")
from Core.models.document import *
from abc import ABC, abstractmethod
class documentRepository():

    @abstractmethod
    def approveDocument(userName:str)->None:
        pass

    @abstractmethod
    def createNewDocument()->str:
        pass
    
    @abstractmethod
    def getAgenda():
        pass

    @abstractmethod
    def allowed_file(filename:str,allowedExtensions:str)->str:
        pass

    @abstractmethod
    def getFolder(reunion_title:str, agenda_title:str, reuniao_id:str , agenda_id:str,upload_folder:str)->str:
        pass

    @abstractmethod
    def getFile(self,reunion_title:str, agenda_title:str, reuniao_id:str, agenda_id:str, document,upload_folder:str)->str:
        pass

    @abstractmethod
    def uploadAgenda(self,reunion_title:str, agenda_title:str, reuniao_id:str, agenda_id:str, document,upload_folder:str)->None:
        pass

    @abstractmethod
    def removeAgendaFiles(self,reunion_title:str, agenda_title:str, reuniao_id:str, agenda_id:str,upload_folder:str)->None:
        pass
 
    

