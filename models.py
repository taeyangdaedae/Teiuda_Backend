from sqlalchemy import Column, String, VARCHAR, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.schema import CreateTable

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    uid = Column('uid',VARCHAR(50),primary_key=True)
    id = Column('id',VARCHAR(20),nullable=False)
    name = Column('name',VARCHAR(10),nullable=False)
    email = Column('email',VARCHAR(50),nullable=False)
    password = Column('password',VARCHAR(100),nullable=False)
    created_at = Column('created_at',DateTime,nullable=True)
    updated_at = Column('updated_at',DateTime,nullable=True)
    
    
class Topic(Base):
    __tablename__ = 'topic'
    
    date = Column('date',Date,primary_key=True)
    topic = Column('topic',VARCHAR(20),nullable=False)
    created_at = Column('created_at',DateTime,nullable=True)

class Think(Base):
    __tablename__ = 'think'
    
    idx = Column('idx',VARCHAR(16),primary_key=True)
    user_uid = Column('user_uid',VARCHAR(50),ForeignKey("user.uid"),nullable = True)
    
    topic_date = Column('topic_table',Date,ForeignKey("topic.date"),nullable = True)
    content = Column('content',VARCHAR(100),nullable=False)
    is_shared = Column('is_shared',TINYINT,nullable=True)
    created_at = Column('created_at',DateTime,nullable=False)
    updated_at = Column('updated_at',DateTime,nullable=True)