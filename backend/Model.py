from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

ma = Marshmallow()
db = SQLAlchemy()

class Sitat(db.Model):
    __tablename__ = 'sitat'
    id = db.Column(db.Integer, primary_key=True)
    sitat = db.Column(db.String(250), nullable=False)
    info = db.Column(db.String(250), nullable=True)
    creation_date = db.Column(db.DateTime, nullable=True)
    barn_id = db.Column(db.Integer, db.ForeignKey('barn.id', ondelete='CASCADE'), nullable=False)
    # barn_id = db.Column(db.Integer, db.ForeignKey('barn.id', ondelete='CASCADE'), nullable=False)
    # barn = db.relationship('Barn', backref=db.backref('sitater', lazy='dynamic' ))
    humoer_id = db.Column(db.Integer, db.ForeignKey('humoer.id', ondelete='CASCADE'), nullable=False)
    # humoer_id = db.Column(db.Integer, db.ForeignKey('humoer.id', ondelete='CASCADE'), nullable=False)
    # humoer = db.relationship('Humoer', backref=db.backref('sitater', lazy='dynamic' ))

    def __init__(self, sitat, barn_id, humoer_id, info, creation_date):
        self.sitat = sitat
        self.barn_id = barn_id
        self.humoer_id = humoer_id
        self.info = info
        self.creation_date = creation_date


class Barn(db.Model):
    __tablename__ = 'barn'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(250), nullable=False)

    def __init__(self, navn):
        self.navn = navn


class Humoer(db.Model):
    __tablename__ = 'humoer'
    id = db.Column(db.Integer, primary_key=True)
    navn = db.Column(db.String(250), nullable=False)
    beskrivelse = db.Column(db.String(350), nullable=True)

    def __init__(self, navn):
        self.navn = navn

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def to_dict(self):
        return dict(id=self.id, email=self.email)

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))

    def __init__(self, jti):
        self.jti = jti

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)




# ---------------- Marshmallow skjema ------------------------------

class SitatSchema(ma.Schema):
    id = fields.Integer(dump_only = True)
    barn_id = fields.Integer(required=True)
    humoer_id = fields.Integer(required=True)
    sitat = fields.String(required=True)
    creation_date = fields.DateTime(allow_none=False, format=None, default=datetime.datetime.utcnow)
    info = fields.String(required=False, allow_none=True)

class BarnSchema(ma.Schema):
    id = fields.Integer(dump_only = True)
    navn = fields.String(required=True)

class HumoerSchema(ma.Schema):
    id = fields.Integer(dump_only = True)
    navn = fields.String(required=True)

class RevokedTokenSchema(ma.Schema):
    jti = fields.String()

class UserSchema(ma.Schema):
    email = fields.String()
    password = fields.String()
