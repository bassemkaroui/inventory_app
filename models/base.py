from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from inventory_app.config import Config

Base = declarative_base()
config = Config()  # type: ignore

engine = create_engine(config.host.unicode_string())


def recreate_tables() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    recreate_tables()
