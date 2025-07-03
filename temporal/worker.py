import asyncio
import logging
from temporalio.client import Client
from temporalio.worker import Worker

from workflows.user_workflow import UserRegisterWorkflow

from activities.user_activities import (
    create_user
)

from config.config import config

logging.basicConfig(level=logging.INFO)

async def main():
    client = await Client.connect(config.TEMPORAL_ADDRESS, namespace=config.TEMPORAL_NAMESPACE)
    # client = await Client.connect("temporal:7233", namespace="default")

    worker = Worker(
        client,
        task_queue="user-creation-queue",
        workflows=[
            UserRegisterWorkflow,
        ],
        activities=[
            create_user, 
        ]
    )

    print("✅ Worker started")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
