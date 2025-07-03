from temporalio import activity
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from dataclasses import dataclass,field
from typing import Optional,List,Dict,Any
@dataclass
class UserInput:
    firstname:str
    lastname:str
    email:str
    mobileNumber:str
    password: str
    password1: str
    middlename: Optional[str] = None
    idProof: Optional[List[Dict[str, Any]]] = field(default_factory=list)
    profilephoto: Optional[Dict[str, Any]] = field(default_factory=dict)
    hobbies: Optional[List[str]] = field(default_factory=list)
    addressInfo: Optional[Dict[str, Any]] = field(default_factory=dict)
    roles: Optional[List[str]] = field(default_factory=list)



# activities/user_activities.py
from temporalio import activity
import httpx

@activity.defn
async def create_user(user_data: dict) -> dict:
    mutation = """
    mutation createuser($data: Createuser!) {
      createuser(data: $data, internal: true) {
        userId
        mobileNumber
      }
    }
    """

    url = "http://user_services:8000/graphql" 

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json={"query": mutation, "variables": {"data": user_data}},
            headers={"Content-Type": "application/json"}
        )

        data = response.json()
        if "errors" in data:
            raise Exception(f"GraphQL error: {data['errors']}")

        user_id = data["data"]["createuser"]["userId"]
        return {"userId": user_id}
