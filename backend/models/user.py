# coding=utf-8

from sqlalchemy import Column, String
from datetime import datetime

from marshmallow import Schema, fields

from .entity import Entity, Base


class User(Entity, Base):
    __tablename__ = 'users'

    nome = Column(String)
    email = Column(String)
    roles = Column(String)

    def __init__(self, nome, email, roles):
        Entity.__init__(self, datetime.now())
        self.nome = nome
        self.email = email
        self.roles = roles

class UserSchema(Schema):
    id = fields.Number()
    nome = fields.Str()
    email = fields.Str()
    roles = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()