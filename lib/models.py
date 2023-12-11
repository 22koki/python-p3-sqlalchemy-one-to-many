from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class TestGame(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    platform = Column(String)
    price = Column(Integer)

    reviews = relationship('Review', back_populates='game')

    def __repr__(self):
        return f'Game(id={self.id}, title={self.title}, platform={self.platform})'

class TestReview(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    comment = Column(String)
    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship('Game', back_populates='reviews')

    def __repr__(self):
        return f'Review(id={self.id}, score={self.score}, game_id={self.game_id})'
