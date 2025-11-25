from models import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///user_data.db", echo=True)
Session  = sessionmaker(bind=engine)
session = Session()