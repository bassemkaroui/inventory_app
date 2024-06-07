from pathlib import Path

# from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(".env/postgres.env")


class Config(BaseSettings):
    host: PostgresDsn

    model_config = SettingsConfigDict(
        env_prefix="postgres_", env_file=env_path, extra="ignore"
    )


# load_dotenv(dotenv_path=env_path)

# DB_NAME = os.getenv('POSTGRES_DB')
# DB_USERNAME = os.getenv('POSTGES_USER')
# DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
# DB_HOST = f'postgres://{DB_USERNAME}:{DB_PASSWORD}@postgresdb:5432/{DB_NAME}'

if __name__ == "__main__":
    config = Config()  # type: ignore
    print(config.host)
