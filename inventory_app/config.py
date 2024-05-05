import os
from dotenv import load_dotenv

env_path = os.path.join(os.getcwd(), '.env/postgres.env')
load_dotenv(dotenv_path=env_path)

class Config:
    DB_NAME = os.getenv('POSTGRES_DB')
    DB_USERNAME = os.getenv('POSTGES_USER')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')

if __name__ == '__main__':
    print(Config.DB_NAME)
    print(Config.DB_USERNAME)
    print(Config.DB_PASSWORD)