from temporalio import workflow
from temporalio.common import RetryPolicy
from datetime import timedelta
from dataclasses import dataclass
from typing import Dict, Any, List

with workflow.unsafe.imports_passed_through():
    from activities.user_activities import create_user, user_maprole, user_profile


@workflow.defn
class UserRegisterWorkflow:
    @workflow.run
    async def run(self, user_data: dict) -> dict:
        retry_policy = RetryPolicy(maximum_attempts=3)

        # Step 1: Create user
        user_result = await workflow.execute_activity(
            create_user,
            user_data,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )
        user_id = user_result["userId"]

        # Step 2: Create user profile
        profile_data = {
            "userId": user_id, 
            "firstname": user_data.get("firstname"),
            "lastname": user_data.get("lastname"),
            "profilephoto": user_data.get("profilephoto"),
            "hobbies": user_data.get("hobbies"),
            "addressinfo": user_data.get("addressInfo"),
        }
        await workflow.execute_activity(
            user_profile,
            profile_data,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )

        # Step 3: Map roles
        role_payload = {
            "userId": user_id,
            "rolename": user_data.get("roles", [])
        }

        mapped_roles: List[Dict[str, int]] = await  workflow.execute_activity(
            user_maprole,
            role_payload,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy
        )
        for role in mapped_roles:
            print("User:", role["userId"], "Role:", role["roleId"])

        # return {"status": "success", "message": "Registration completed", "user_id": user_id}
        return user_result
