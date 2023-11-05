import datetime
from uuid import uuid4

class Document:
    id: str
    meetingId: str
    title: str
    path: str
    date: datetime
    approved: bool
    comment: str
    reqUserId:str

    def __init__(self, id, meetingId, title, path, approved, comment, reqUserId):
        self.id = id
        self.title = title
        self.meetingId=meetingId
        self.approved=approved
        self.path=path
        self.comment = comment
        self.reqUserId=reqUserId

    
def documentFactory(meetingId:str = "",title:str="",path:str="",approved:bool=True, reqUserId:str="", comment:str = "", id:str=str(uuid4)) -> Document:
    return Document(id=id, meetingId=meetingId,title=title,approved=approved,path=path,reqUserId=reqUserId, comment=comment)