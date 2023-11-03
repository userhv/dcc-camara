import datetime
from uuid import uuid4

class Meeting:
    def __init__(self, id_, title, date, role):
        self.id_ = id_
        self.title = title
        self.date = date
        self.role = role


def meetingFactory(title: str,date: datetime,role="") -> Meeting:
    return Meeting(id_=str(uuid4), title=title,date=date,role=role)