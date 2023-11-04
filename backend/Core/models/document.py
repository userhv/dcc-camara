import datetime
from uuid import uuid4

class Document:
    id: str
    meetingId: str
    title: str
    path: str
    date: datetime
    approved: bool
    def __init__(self, id, meetingId, title, path,approved):
        self.id = id
        self.title = title
        self.meetingId=meetingId
        self.approved=approved
        self.path=path

    
def documentFactory(meetingId:str,title:str,path:str,approved:bool) -> Document:
    return Document(id=str(uuid4), meetingId=meetingId,title=title,approved=approved,path=path)