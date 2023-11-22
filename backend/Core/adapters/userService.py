import sys
from backend.Core.models.user import User
sys.path.insert(0,"..")
from backend.Core.ports.userRepo import userRepository
import psycopg2
import jwt

class userSerivce(userRepository):

    def getUserId(token:str, secretKey: str)->int:
        decoded_token = jwt.decode( token,secretKey, algorithms=['HS256'])
        return decoded_token["unique_id"]
    
    def getUserInfo(token:str,secretKey:str)->dict:
        decoded_token = jwt.decode( token,secretKey, algorithms=['HS256'])
        return {'username':decoded_token['user_id'], 'role':decoded_token['user_type']}

    def loginUser(userName:str,secretKey:str,conn)-> dict:
       
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nome,role,id FROM usuario WHERE nome = %s", (userName,))
        user = cursor.fetchone()
        cursor.close()

        if user is None:
            return {'acess_token':"",'user_type':""}

        user_id = user[0]
        user_type = user[1]
        unique_id = user[2]

        token = jwt.encode({'user_id': user_id, 'user_type': user_type,"unique_id":unique_id}, secretKey, algorithm='HS256')

        return{'access_token': token, "user":user_id, "user_type":user_type}
