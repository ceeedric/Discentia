from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

engine = create_engine('postgresql://discentia:discentia@127.0.0.1:5432/discentia')
session = sessionmaker(bind=engine)


