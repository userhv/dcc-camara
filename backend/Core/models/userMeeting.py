
from uuid import uuid4

class UserMeeting:
    userId: str
    meetingId: str
  

def userMeetingFactory(userId: str, meetingId )-> UserMeeting:
    return UserMeeting( userId=userId, meetingId=meetingId)