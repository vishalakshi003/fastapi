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
@activity.defn
async def delete_user(id:int)->None:
    mutation=gql("""
    mutation deleteuser($id:Int!){
        deleteuser(id:$id){
                 success
                 error
                 }
                 }
""")
    async with get_gql_client() as client:
        results=await client.execute(mutation,variable_values={"id": id})
        data = results["deleteuser"]

        if not data["success"]:
            if data["error"]:
                activity.logger.info(f"User {id} already deleted")

            else:
                activity.logger.warning(f"Failed to delete user {id}: {data['error']}")

        # return data["success"]

@activity.defn
async def user_profile(payload: dict) -> dict:
    mutation =gql( """
    mutation createuserprofile($data: UserProfileInput!) {
        createuserprofile(data: $data,internal: true) {
                id
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
@activity.defn
async def delete_userprofile(id:int)->None:
    mutation=gql("""
    mutation deleteuserprofile($id:Int!){
        deleteuserprofile(id:$id){
                 success
                 error
                 }
                 }
""")
    async with get_gql_client() as client:
        results=await client.execute(mutation,variable_values={"id": id})
        data = results["deleteuserprofile"]

        if not data["success"]:
            if data["error"]:
                activity.logger.info(f"User {id} already deleted")

            else:
                activity.logger.warning(f"Failed to delete user {id}: {data['error']}")


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

@activity.defn
async def delete_userrolemap(id:int)->None:
    mutation=gql("""
    mutation deleteuserrolemap($id:Int!){
        deleteuserrolemap(id:$id){
                 success
                 error
                 }
                 }
""")
    async with get_gql_client() as client:
        results=await client.execute(mutation,variable_values={"id": id})
        data = results["deleteuserrolemap"]

        if not data["success"]:
            if data["error"]:
                activity.logger.info(f"User {id} already deleted")
            else:
                activity.logger.warning(f"Failed to delete user {id}: {data['error']}")

