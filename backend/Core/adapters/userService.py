import sys
from Core.models.user import User
sys.path.insert(0,"..")
from Core.ports.userRepo import userRepository
import psycopg2
import jwt

class userSerivce(userRepository):

    def getUserInfo(token:str,secretKey:str)->dict:
        
        conn = psycopg2.connect(host='localhost',
                            database='camara_db',
                            user='admin',
                            password='123456')
        cursor = conn.cursor()
        decoded_token = jwt.decode( token,secretKey, algorithms=['HS256'])
        return {'username':decoded_token['user_id'],'role':decoded_token['user_type']}

    def loginUser(userName:str,secretKey:str)-> dict:
        conn =  psycopg2.connect(host='localhost',
                            database='camara_db',
                            user='admin',
                            password='123456')

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
