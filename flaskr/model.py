from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return '<Language %r>' % self.name
