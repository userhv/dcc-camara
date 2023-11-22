import unittest
from unittest.mock import MagicMock, patch
import sys
sys.path.insert(0,"..")
sys.path.insert(0,"../..")
import jwt
from adapters.userService import *  

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
        expected={'access_token':"",'user_type':""}
        self.assertEqual(token, expected)



if __name__ == '__main__':
    unittest.main()