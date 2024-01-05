from sqlalchemy import Column, String, VARCHAR, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql
from sqlalchemy.schema import CreateTable

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    uid = Column('uid',VARCHAR(8),primary_key=True)
    id = Column('id',VARCHAR(20),nullable=False)
    name = Column('name',VARCHAR(10),nullable=False)
    email = Column('email',VARCHAR(20),nullable=False)
    password = Column('password',VARCHAR(10),nullable=False)
    created_at = Column('created_at',DateTime,nullable=True)
    updated_at = Column('updated_at',DateTime,nullable=True)
    
    
class Topic(Base):
    __tablename__ = 'topic'
    
    date = Column('date',Date,primary_key=True)
    topic = Column('topic',VARCHAR(20),nullable=False)
    created_at = Column('created_at',DateTime,nullable=True)
    