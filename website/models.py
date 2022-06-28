# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 17:26:24 2022

@author: shrey
"""

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# for storing reminders
# class Reminder(db.Model):
    
    

class User(db.Model, UserMixin):
    # defining all the columns we want in our database
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    #notes = db.relationship('Note') # this will be like a list to store the note id for every user
    