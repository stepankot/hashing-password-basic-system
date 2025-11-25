from models import Base, User
from config import engine

if __name__ == '__main__':
    Base.metadata.create_all(engine)