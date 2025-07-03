from dotenv import load_dotenv
import os
load_dotenv()

class Config():
    def __init__(self):
        self.DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
        self.JWT_SECRET = os.getenv("JWT_SECRET", "mysecretkey")
        
        # Temporal
        self.TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
        self.TEMPORAL_NAMESPACE = os.getenv("TEMPORAL_NAMESPACE", "default")
        self.TEMPORAL_TASK_QUEUE = os.getenv("TEMPORAL_TASK_QUEUE", "user-creation-queue")

# Initialize once globally
config = Config()
