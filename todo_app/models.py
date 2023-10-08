from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()  

class Task(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable = False)
    Status = db.Column(db.Boolean, nullable = False)
    
    def __repr__(self):
        return f'<{self.title}:{self.status}>'