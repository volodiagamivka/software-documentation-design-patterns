from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    email = Column(String)
    sessions = relationship("GameSession", back_populates="user")

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String)
    type = Column(String)
    price = Column(Float, default=0.0)
    __mapper_args__ = {'polymorphic_on': type, 'polymorphic_identity': 'game'}

class FreeGame(Game):
    __mapper_args__ = {'polymorphic_identity': 'free'}

class PaidGame(Game):
    __mapper_args__ = {'polymorphic_identity': 'paid'}

class GameSession(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    game_id = Column(Integer, ForeignKey('games.id'))
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    current_progress = Column(String)
    user = relationship("User", back_populates="sessions")