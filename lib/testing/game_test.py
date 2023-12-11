import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conftest import SQLITE_URL
from ..models import Game, Review

@pytest.fixture
def session():
    engine = create_engine(SQLITE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # Teardown: rollback the session to leave the database in a clean state
    session.rollback()
    session.close()

class TestGame:
    @staticmethod
    def create_test_data(session):
        mario_kart = Game(
            title="Mario Kart",
            platform="Switch",
            genre="Racing",
            price=60
        )

        session.add(mario_kart)
        session.commit()

        mk_review_1 = Review(
            score=10,
            comment="Wow, what a game",
            game_id=mario_kart.id
        )

        mk_review_2 = Review(
            score=8,
            comment="A classic",
            game_id=mario_kart.id
        )

        session.bulk_save_objects([mk_review_1, mk_review_2])
        session.commit()

        return mario_kart

    def test_game_has_correct_attributes(self, session):
        '''has attributes "id", "title", "platform", "genre", "price".'''
        mario_kart = self.create_test_data(session)
        assert all(
            hasattr(mario_kart, attr) for attr in ["id", "title", "platform", "genre", "price"]
        )

    def test_has_associated_reviews(self, session):
        '''has two reviews with scores 10 and 8.'''
        mario_kart = self.create_test_data(session)
        assert (
            len(mario_kart.reviews) == 2
            and mario_kart.reviews[0].score == 10
            and mario_kart.reviews[1].score == 8
        )
