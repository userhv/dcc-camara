import unittest
from unittest.mock import MagicMock, patch
import sys
sys.path.insert(0,"..")
sys.path.insert(0,"../..")

from adapters.meetingService import *  


class TestMeetingService(unittest.TestCase):
    def test_getMeetingTitle_success(self):
        magic_conn = MagicMock()
        magic_conn.cursor.return_value = magic_conn
        expected ='Meeting Title'
        magic_conn.fetchone.return_value = [expected]
        meeting = meetingSerivce.getMeetingTitle(12,magic_conn)
        self.assertEqual(meeting,expected)

    def test_getMeetingTitle_error(self):
        magic_conn = MagicMock()
        magic_conn.cursor.return_value = magic_conn
        magic_conn.fetchone.return_value = [None]
        meeting = meetingSerivce.getMeetingTitle(12,magic_conn)
        expected ='Meeting not Found'
        self.assertEqual(meeting,expected)

    @patch("jwt.decode")
    def test_createNewMeeting_success(self,mock_jwt_encode):
        title = "Meeting Title"
        date = "01/01/2000"
        token = "any"
        secretKey = "any"
        mock_jwt_encode.return_value = {"user_type":"Chefia"}
        meeting = meetingSerivce.createNewMeeting(title,date,token,secretKey)
        self.assertEqual(title,meeting.title)
        self.assertEqual(date,meeting.date)

    @patch("jwt.decode")
    def test_createNewMeeting_error(self,mock_jwt_encode):
        title = "Meeting Title"
        date = "01/01/2000"
        token = "any"
        secretKey = "any"
        mock_jwt_encode.return_value = {"user_type":"Discente"}
        with self.assertRaises(PermissionError) as context:
            meeting = meetingSerivce.createNewMeeting(title,date,token,secretKey)
        raised_exception = context.exception
        self.assertEqual(str(raised_exception), "Only Chefia role allowed")
        
       
       

      