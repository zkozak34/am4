import os
import sqlalchemy as sa

# create base
Base = sa.orm.declarative_base()

class Users(Base):
    __tablename__ = "airports"

class DB():
    def __init__(self):
        # check if db.sqlite exists
        self.db = sa.create_engine('sqlite:///db.sqlite')
        if not os.path.isfile('db.sqlite'):
            print('Creating new database')
            self.db.create_all()