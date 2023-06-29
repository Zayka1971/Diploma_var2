import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from config import db_url_object

metadata = MetaData()
Base = declarative_base()


class Viewed(Base):
    __tablename__ = 'vk_views'

    id = sq.Column(sq.Integer, primary_key=True)
    profile_id = sq.Column(sq.Integer)
    worksheet_id = sq.Column(sq.Integer, unique=True)

    engine = create_engine(db_url_object)


def create_tables(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(autoflush=False, bind=engine)
    session = Session()
    with Session as session:
        to_bd = Viewed(profile_id=1, worksheet_id=1)
    session.add(to_bd)
    session.commit()
