from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.models import Base
from dal.repository import SqlAlchemyRepository
from dal.csv_loader import CsvLoader 
from bll.services import ImportService

def bootstrap():
    engine = create_engine('sqlite:///data/steam.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    repo = SqlAlchemyRepository(Session())
    loader = CsvLoader() 
    service = ImportService(repo, loader)

    
    service.execute_import('data/data.csv')
    print("system  completed importing data from CSV to database")

if __name__ == "__main__":
    bootstrap()