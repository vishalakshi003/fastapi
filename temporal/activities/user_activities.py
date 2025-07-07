from temporalio import activity
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from dataclasses import dataclass,field
from typing import Optional,List,Dict,Any
from .dataclass_input import *

# activities/user_activities.py
from temporalio import activity
# import httpx
from gql.transport.exceptions import TransportQueryError


GRAPHQL_URL = "http://user_services:8000/graphql"

# create GraphQL client
def get_gql_client():
    transport = AIOHTTPTransport(url=GRAPHQL_URL)
    return Client(transport=transport, fetch_schema_from_transport=True)

@activity.defn
async def create_user(user_data: dict) -> dict:
    mutation = gql("""
    mutation createuser($data: Createuser!) {
      createuser(data: $data, internal: true) {
        userId
        mobileNumber
      }
    }
    """)

    async with get_gql_client() as client:
        try:
            result = await client.execute(mutation, variable_values={"data": user_data})
            return {
                "userId": result["createuser"]["userId"],
                "mobileNumber": result["createuser"]["mobileNumber"]
            }
        except TransportQueryError as e:
            raise Exception(f"GraphQL error: {e.errors}")

    # url = "http://user_services:8000/graphql" 

    # async with get_gql_client() as client:
    #     response = await client.post(
    #         url,
    #         json={"query": mutation, "variables": {"data": user_data}},
    #         headers={"Content-Type": "application/json"}
    #     )

    #     data = response.json()
    #     if "errors" in data:
    #         raise Exception(f"GraphQL error: {data['errors']}")

    #     user_id = data["data"]["createuser"]["userId"]
    #     return {"userId": user_id}


@activity.defn
async def user_profile(payload: dict) -> dict:
    mutation =gql( """
    mutation createuserprofile($data: UserProfileInput!) {
        createuserprofile(data: $data,internal: true) {
          userId
          firstname
        }
      }""")
          

    async with get_gql_client() as client:
        try:
            result = await client.execute(mutation, variable_values={"data": payload})
            return result["createuserprofile"]
        except TransportQueryError as e:
            raise Exception(f"GraphQL error: {e.errors}")
    # url = "http://user_services:8000/graphql"
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         url,
    #         json={
    #             "query": mutation,
    #             "variables": {
    #                 "data":payload
    #             }
    #         },
    #         headers={"Content-Type": "application/json"}
    #     )

    #     data = response.json()
    #     if "errors" in data:
    #         raise Exception(f"GraphQL error: {data['errors']}")

    #     return data["data"]["createuserprofile"]

@activity.defn
async def user_maprole(payload: dict) -> List[Dict[str, int]]:
    mutation = gql("""
    mutation maprolestouser($data: RoleMappingInput!) {
      maprolestouser(data: $data,internal: true) {
        id
        userId
        roleId
      }
    }
    """)
    variables = {
        "data": {
            "userId": payload["userId"],
            "rolename": payload["rolename"]
        }
    }
    async with get_gql_client() as client:
        try:
            result = await client.execute(mutation, variable_values=variables)
            mapping_data=result["maprolestouser"]
            return mapping_data
        except TransportQueryError as e:
            raise Exception(f"GraphQL error: {e.errors}")

    # url = "http://user_services:8000/graphql"
    # async with httpx.AsyncClient() as client:
    #     response = await client.post(
    #         url,
    #         json={
    #             "query": mutation,
    #             "variables": {
    #                 "data": {
    #                     "userId": payload["userId"],
    #                     "rolename": payload["rolename"]
    #                 }
    #             }
    #         },
    #         headers={"Content-Type": "application/json"}
    #     )

    #     data = response.json()
    #     if "errors" in data:
    #         raise Exception(f"GraphQL error: {data['errors']}")
    #     mapping_data=data["data"]["maprolestouser"]
    #     return mapping_data 
