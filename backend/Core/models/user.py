
from uuid import uuid4

class User:
    id: str
    userName: str
    role: str
    

def userFactory(userName: str, role: str) -> User:
    return User(id_=str(uuid4), userName=userName, role=role)