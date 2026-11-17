import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY', 'warehouse-logistic-secret-key-98765')
ALGORITHM = "HS256"
