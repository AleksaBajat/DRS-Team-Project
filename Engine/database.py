from sqlalchemy import create_engine

from models import Base


def main():
    engine = create_engine("sqlite:///mydb.db", echo=True)
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    main()