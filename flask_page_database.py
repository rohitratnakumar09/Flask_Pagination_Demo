from sqlalchemy import Column,ForeignKey,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base=declarative_base()
class Book(Base):
    __tablename__='book'
    id=Column(Integer,primary_key=True)
    title=Column(String(250),nullable=False)
    author=Column(String(250),nullable=False)
    genre=Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'genre':self.genre
        }
dbpath='sqlite:///books-collection.db?check_same_thread=False'
engine=create_engine(dbpath)
Base.metadata.create_all(engine)