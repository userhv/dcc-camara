import sys
from Core.models.userMeeting import *
sys.path.insert(0,"..")
from ports.userMeetingRepo import *
import psycopg2
import jwt

class userMeetingService(userMeetingRepository):
        pass
