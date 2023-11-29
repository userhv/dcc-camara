import unittest
from unittest.mock import MagicMock, patch
import sys
sys.path.insert(0,"..")
sys.path.insert(0,"../..")
import jwt
from backend.Core.adapters.userService import *  

class TestUserService(unittest.TestCase):
    def test_login_user_successful(self):
      
        magic_conn = MagicMock()
        magic_conn.cursor.return_value = magic_conn
        magic_conn.fetchone.return_value = ('John Doe', 'Chefia', 1)
        token = userSerivce.loginUser('John Doe', '12345',magic_conn)
        token = token['access_token']
        decoded_token = jwt.decode(token,'12345' , algorithms=['HS256'])
        expected_decoded ={'user_id':'John Doe','user_type':"Chefia","unique_id":1}
        self.assertEqual(decoded_token, expected_decoded)

    def test_login_user_error(self):
        magic_conn = MagicMock()
        magic_conn.cursor.return_value = magic_conn
        magic_conn.fetchone.return_value = None
        token = userSerivce.loginUser('John Does', '12345',magic_conn)
        expected= {'acess_token':"",'user_type':""}
        self.assertEqual(token, expected)

    @patch("jwt.decode")
    def test_getUserId_success(self, mock_jwt_decode):
        # Configuração do mock para jwt.decode
        mock_jwt_decode.return_value = {"unique_id": 1}

        # Execução da função a ser testada
        result = userSerivce.getUserId("any_token", "any_secret")

        # Verificação dos resultados esperados
        expected_result = 1
        self.assertEqual(result, expected_result)

    @patch("jwt.decode")
    def test_getUserInfo_success(self, mock_jwt_decode):
        # Configuração do mock para jwt.decode
        mock_jwt_decode.return_value = {"user_id": "John Doe", "user_type": "Chefia"}

        # Execução da função a ser testada
        result = userSerivce.getUserInfo("any_token", "any_secret")

        # Verificação dos resultados esperados
        expected_result = {'username': 'John Doe', 'role': 'Chefia'}
        self.assertEqual(result, expected_result)


