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
    def getDocuments()->dict:
        pass
