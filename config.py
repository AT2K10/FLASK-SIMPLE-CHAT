import dotenv
import os

dotenv.load_dotenv()
class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI')
    API_KEY=os.environ.get('API_KEY')