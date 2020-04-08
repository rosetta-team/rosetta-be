from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://postgres:postgres@localhost:5432/rosetta_dev", convert_unicode=True)
# engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base  = declarative_base()

Base.query = db_session.query_property()

# Define models in relation to instantiated ORM
class Method(Base):
    __tablename__ = 'methods'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    snippet = Column(Text)
    syntax = Column(Text)
    description = Column(Text)
    docs_url = Column(String)
    language_id = Column(Integer, ForeignKey('languages.id'))

    def __repr__(self):
        return '<Method %r>' % self.name

class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    methods = relationship(
        Method,
        backref=backref(
            'language',
            uselist=True,
            cascade=('delete, all')
        )
    ) 

    def __repr__(self):
        return '<Language %r>' % self.name