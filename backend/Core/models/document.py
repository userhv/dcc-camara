import datetime
from uuid import uuid4

class Document:
    id: str
    meetingId: str
    title: str
    path: str
    date: datetime
    approved: bool
    def __init__(self, id, meetingId, title, path,date,approved):
        self.id = id
        self.title = title
        self.date = date
        self.meetingId=meetingId
        self.path=path
        self.approved=approved

    
def documentFactory(meetingId:str,title: str,path:str,date: datetime,approved:bool) -> Document:
    return Document(id_=str(uuid4), meetingId=meetingId,path=path,title=title,date=date,approved=approved)