from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from dataclasses import dataclass,field
from typing import Dict, List, Optional,Any
with workflow.unsafe.imports_passed_through():
    from activities.user_activities import create_user

@workflow.defn
class UserRegisterWorkflow:
    @workflow.run
    async def run(self, user_data: Dict) -> Dict:
        result = await workflow.execute_activity(
            create_user,
            user_data,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(
                maximum_attempts=3
            )
        )
        print('result-----------------------',result)
        return result