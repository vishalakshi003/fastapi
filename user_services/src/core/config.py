from dotenv import load_dotenv
import os
load_dotenv()

class Config():
    DATABASE_URL=os.getenv("DATABASE_URL")
    JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
    JWT_SECRET=os.getenv("JWT_SECRET")