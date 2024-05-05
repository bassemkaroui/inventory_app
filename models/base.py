from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from inventory_app.config import Config

Base = declarative_base()
config = Config()

engine = create_engine(config.host.unicode_string(), echo=True)

def recreate_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)