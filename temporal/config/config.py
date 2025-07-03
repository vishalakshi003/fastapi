import os
# os.environ["TEMPORAL_HOST"] = "temporal:7233"
class Config:
    def __init__(self):
        self.TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "temporal:7233")
        self.TEMPORAL_NAMESPACE = os.getenv("TEMPORAL_NAMESPACE", "default")
        self.TEMPORAL_TASK_QUEUE = os.getenv("TEMPORAL_TASK_QUEUE", "user-creation-queue")

config = Config()
