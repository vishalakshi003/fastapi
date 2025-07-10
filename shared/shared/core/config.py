from pathlib import Path
from dotenv import load_dotenv
import os

#if we use this , it take user_servce/env file 
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

# load_dotenv()

class Config:
    def __init__(self):
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
        self.JWT_SECRET = os.getenv("JWT_SECRET", "mysecretkey")
        self.TOKEN_EXPIRE_DAYS = int(os.getenv("TOKEN_EXPIRE_DAYS", "1"))
config=Config()