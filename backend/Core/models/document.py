import datetime
from uuid import uuid4

class Document:
    id: str
    meetingId: str
    title: str
    path: str
    date: datetime
    approved: bool
    reqUserId:str
    def __init__(self, id, meetingId, title, path,approved,reqUserId):
        self.id = id
        self.title = title
        self.meetingId=meetingId
        self.approved=approved
        self.path=path
        self.reqUserId=reqUserId

    
def documentFactory(meetingId:str,title:str,path:str,approved:bool,reqUserId:str) -> Document:
    return Document(id=str(uuid4), meetingId=meetingId,title=title,approved=approved,path=path,reqUserId=reqUserId)