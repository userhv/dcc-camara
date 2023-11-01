# coding=utf-8

from flask import Flask, jsonify, request

from models.entity import Session, engine, Base
from models.user import User, UserSchema

# creating the Flask application
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# if needed, generate database schema
Base.metadata.create_all(engine)
session = Session()


def add_users():
    # create and persist mock exam

    users = session.query(User).all()
    if len(users) == 0:
        python_exam = User("Fernando", "email@discente.com", "Representante Discente")
        session.add(python_exam)
        session.commit()
        python_exam = User("Carlos", "email@chefia.com", "Chefia")
        session.add(python_exam)
        session.commit()
    
    # reload exams

@app.route('/users',methods=['GET'])
def get_users():
    # fetching from the database
    users = session.query(User).all()
    result = UserSchema.dump(users)
    return jsonify(result)


if __name__ == '__main__':
    add_users()
    app.run(debug=True, port=8080)



