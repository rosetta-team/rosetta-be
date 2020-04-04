from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.column(db.String(50), nullable=False, unique=True)
