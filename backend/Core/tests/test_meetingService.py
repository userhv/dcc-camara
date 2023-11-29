import unittest
from unittest.mock import MagicMock, patch
import sys
sys.path.insert(0,"../..")

from backend.Core.adapters.meetingService import *  


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
        
    @patch("jwt.decode")
    @patch("psycopg2.connect")
    def test_getMeetingInfo_success(self, mock_connect, mock_jwt_decode):
        # Configuração do mock para jwt.decode
        mock_jwt_decode.return_value = {"user_id": 1}

        # Configuração do mock para psycopg2.connect
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [(1, "Title 1", "2023-01-01")]

        # Configuração do token e chave secreta (não são usados, mas são necessários)
        token = "any_token"
        secret_key = "any_secret"

        # Execução da função a ser testada
        result = meetingSerivce.getMeetingInfo(token, secret_key)

        # Verificação dos resultados esperados
        expected_result = {'data': [(1, "Title 1", "2023-01-01")]}
        self.assertEqual(result, expected_result)

    @patch("psycopg2.connect")
    def test_insertDB_success(self, mock_connect):
        # Configuração do mock para psycopg2.connect
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = [1]

        # Criação de um objeto Meeting fictício
        meeting = MagicMock()
        meeting.title = "Title 1"
        meeting.date = "2023-01-01"

        # Execução da função a ser testada
        result = meetingSerivce.insertDB(meeting, mock_conn)

        # Verificação dos resultados esperados
        expected_result = {"id_reuniao": 1}
        self.assertEqual(result, expected_result)
       

      