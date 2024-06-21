from datetime import datetime
from .extensions import db

task_drones = db.Table('task_drones',
    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
    db.Column('drone_id', db.Integer, db.ForeignKey('drone.id'), primary_key=True)
)

class Drone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    drones = db.relationship('Drone', secondary=task_drones, lazy='subquery',
                             backref=db.backref('tasks', lazy=True))

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task = db.relationship('Task', backref=db.backref('images', lazy=True))
    image_name = db.Column(db.String(100), nullable=False)
    capture_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    drone_id = db.Column(db.Integer, nullable=False)
