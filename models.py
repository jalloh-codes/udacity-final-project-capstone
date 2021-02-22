
import os
from sqlalchemy import Column, String, Integer, Boolean, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import relationship, sessionmaker
import json, sys


database_path= os.getenv('DATABASE_URI')
if not database_path:
    database_path = database_path = 'postgres://hllanhox:gUGLEZB43EJ7YDV0XRV8V9pefd3SyKB1@ziggy.db.elephantsql.com:5432/hllanhox'

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
    #db.create_all()


# Models
class Leader(db.Model):
    __tablename__ = 'leaders'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    firstname =  db.Column(db.String(50))
    lastname =  db.Column(db.String(50))
    members = db.relationship('Member', backref='leaders', lazy=True)
    projects = db.relationship('Project', backref='leaders', lazy=True)

    def __repr__(self):
        return f'<Leader {self.id} {self.email}>'


    '''
    add a new leader
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def long(self):
        return{
        'id': self.id,
        'email': self.email,
        'firstname': self.firstname,
        'lastname': self.lastname,
    }

# member model
class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    leader_id = db.Column(db.Integer, db.ForeignKey('leaders.id'), nullable=False)
    # projects =  db.relationship('Project', backref='members', lazy=True)
    tasks = db.relationship('Task', backref='members', lazy=True)

    def __repr__(self):
        return f'<Member {self.id} {self.email}>'

        '''
    add a new member
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def long(self):
        return{
        'id': self.id,
        'email': self.email,
        'firstname': self.firstname,
        'lastname': self.lastname,
        'leader_id': self.leader_id
    }


# project model
class Project(db.Model):
    __tablename__ = 'projects'
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    about = db.Column(db.String(500))
    complete = db.Column(db.Boolean(), default=False)
    leader_id = db.Column(db.Integer, db.ForeignKey('leaders.id'), nullable=False)
    # member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    tasks = db.relationship('Task', backref='tasks', lazy=True)

    def __repr__(self):
        return f'<Project {self.id}  {self.name} {self.complete}>'

    '''
    add a new project
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update project info
    '''
    def update(self):
        db.session.commit()

    def long(self):
        return{
            'id': self.id,
            'name': self.name,
            'about': self.about,
            'complete': self.complete,
            'leader_id': self.leader_id
        }


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    details = db.Column(db.String(500))
    complete = db.Column(db.Boolean(), default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.id} {self.name} {self.complete}>'

    '''
    add a new project
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update tast info
    '''
    def update(self):
        db.session.commit()

    '''
    delelte task
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()



    def long(self):
        return{
            'id': self.id,
            'name': self.name,
            'details': self.details,
            'complete': self.complete,
            'project_id': self.project_id,
            'member_id': self.member_id
        }



