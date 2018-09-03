from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import datetime

ma = Marshmallow()
db = SQLAlchemy()

class Sitat(db.Model):
    __tablename__ = 'sitat'
    id = db.Column(db.Integer, primary_key=True)
    sitat = db.Column(db.String(250), nullable=False)
    info = db.Column(db.String(250), nullable=True)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    barn_id = db.Column(db.Integer, db.ForeignKey('barn.id', ondelete='CASCADE'), nullable=False)
    # barn_id = db.Column(db.Integer, db.ForeignKey('barn.id', ondelete='CASCADE'), nullable=False)
    # barn = db.relationship('Barn', backref=db.backref('sitater', lazy='dynamic' ))
    humoer_id = db.Column(db.Integer, db.ForeignKey('humoer.id', ondelete='CASCADE'), nullable=False)
    # humoer_id = db.Column(db.Integer, db.ForeignKey('humoer.id', ondelete='CASCADE'), nullable=False)
    # humoer = db.relationship('Humoer', backref=db.backref('sitater', lazy='dynamic' ))

    def __init__(self, sitat, barn_id, humoer_id, info):
        self.sitat = sitat
        self.barn_id = barn_id
        self.humoer_id = humoer_id
        self.info = info

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



# ---------------- Marshmallow skjema ------------------------------

class SitatSchema(ma.Schema):
    id = fields.Integer(dump_only = True)
    barn_id = fields.Integer(required=True)
    humoer_id = fields.Integer(required=True)
    sitat = fields.String(required=True)
    creation_date= fields.DateTime(dump_only = True, format = None)
    info = fields.String(required=False, allow_none=True)

class BarnSchema(ma.Schema):
    id = fields.Integer(dump_only = True)
    navn = fields.String(required=True)

class HumoerSchema(ma.Schema):
    id = fields.Integer(dump_only = True)
    navn = fields.String(required=True)
