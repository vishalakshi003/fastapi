from datetime import datetime
import strawberry
import temporalio
from temporalio.common import WorkflowIDReusePolicy
from temporalio.exceptions import WorkflowAlreadyStartedError
from src.schemas.user_schema import *
from src.core.config import config
from .types import Create_role,Get_role,Create_user, LoginReq,ResponseMessage,Create_Lang,GetLang, SuccessResponse, TokenRes, User_details, UserCreateResponse
from ...models.rolemaster import RoleMaster
from ...models.customuser import CustomUser
from ...models.rolemapping import RoleMapping
from ... models.user_profile import UserPersonalProfile
from ...models.language import Language,language_users
from ...dependency import SessionDeps
from sqlalchemy import Boolean, insert, select
from fastapi import HTTPException,status
from ...utils import generate_access_token, password_context
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.exceptions import GraphQLError
from temporalio.client import Client
import uuid


@strawberry.type
class Mutations():
    @strawberry.mutation
    async def Createrole(self,info:Info,data:Create_role)->Get_role:
        db: AsyncSession = info.context["db"]
        validated =CreateRole(**data.__dict__)
        results=await db.execute(select(RoleMaster).where(RoleMaster.name==validated.name))
        role_exists=results.scalar()
        if role_exists:
            raise HTTPException(status_code=400,detail='role already exists')
        roles=RoleMaster(name=validated.name,desc=validated.desc)
        db.add(roles)
        await db.commit()
        await db.refresh(roles)
        return roles
    
    @strawberry.mutation
    async def CreateUserInDB(self,info:Info,data:Create_user)->UserCreateResponse:

        try:
            #inject dependenceny for db
            db: AsyncSession = info.context["db"]
            #validate fields with pydantic schemas
            validated = CreateUser(**data.__dict__)
            async with db.begin():
                if validated.password != validated.password1:
                    raise GraphQLError('enter correct password',extensions={"status_code":400})
                hash_password=password_context.hash(validated.password)
                emails_exists_res=await db.execute(select(CustomUser).where(CustomUser.email==validated.email))
                email_exists=emails_exists_res.scalar_one_or_none()
                if email_exists:
                    raise GraphQLError('email already exists',extensions={"status_code":400})
                
                users=CustomUser(email=validated.email,mobile_number=validated.mobileNumber,password=hash_password)
                db.add(users)
                await db.flush()

                profile=UserPersonalProfile(firstname=validated.firstname,lastname=validated.lastname,user_id=users.id,created_by=str(users.id))
                db.add(profile)

                role_res=await db.execute(select(RoleMaster).where(RoleMaster.name.in_(validated.roles)))
                if not role_res:
                    raise HTTPException(status_code=400,detail='role not found')
                roles=role_res.scalars()
                for role in roles:
                    db.add(RoleMapping(user_id=users.id,role_id=role.id))
                if data.language:
                    lang_res=await db.execute(select(Language).where(Language.name.in_(validated.language)))
                    language=lang_res.scalars()
                    for lang in language:
                        await db.execute(insert(language_users).values(user_id=users.id,language_id=lang.id))
                await db.refresh(users)
                await db.refresh(profile)
                return UserCreateResponse(
                status="success",
                message="User created successfully",
                userId=str(users.id)
            )
        except GraphQLError as gql_error:
            #  Preserve the actual GraphQL error
            raise gql_error  
        except Exception as e:
            await db.rollback()
            raise GraphQLError(f"Something went wrong :{str(e)}")

    @strawberry.mutation
    async def CreateLanguage(self,info:Info,data:Create_Lang)->GetLang:
        try:
            db:AsyncSession=info.context["db"]
            user=info.context["user"]
            if not user:
                raise GraphQLError('not unthorized')
            lang=Language(name=data.name,created_by=str(1))
            db.add(lang)
            await db.commit()
            await db.refresh(lang)
            return lang
        except GraphQLError as gql_error:
            #  Preserve the actual GraphQL error
            raise gql_error  
        except Exception as e:
            await db.rollback()
            raise GraphQLError(f"Something went wrong :{str(e)}")
    @strawberry.mutation
    async def Loginapi(self,info:Info,request:LoginReq)->TokenRes:
        try:
            db:AsyncSession=info.context["db"]
            results=await db.execute(select(CustomUser).filter(CustomUser.mobile_number==request.mobile_no))
            users=results.scalar()
            if not users or not password_context.verify(request.password,users.password):
                raise GraphQLError('mobile no or password is invalid')
            token = generate_access_token(data={
            "user":{
                    "id":users.id,
                    "email":users.email,
                },})
            return TokenRes(
                status=SuccessResponse(
                    status="success",
                    message="Login successful",
                    status_code=200
                ),token= token)
        except GraphQLError as gql_error:
            raise gql_error  
        except Exception as e:
            print('error',str(e))
            raise GraphQLError(f"Something went wrong :{str(e)}")

    @strawberry.mutation
    async def createuser(self,data: Create_user,info:Info,internal:bool=False) -> User_details:

        if not internal:
            try:
                user_data = CreateUser(**data.__dict__)

                client = await Client.connect(config.TEMPORAL_ADDRESS, namespace=config.TEMPORAL_NAMESPACE)

                workflow_id = f"user-register--{user_data.mobileNumber}"

                handle = await client.start_workflow(
                    "UserRegisterWorkflow", 
                    user_data.dict(),       
                    id=workflow_id,
                    task_queue=config.TEMPORAL_TASK_QUEUE,
                    id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE_FAILED_ONLY,
                )
            except WorkflowAlreadyStartedError:
                raise GraphQLError("Workflow already started. Please wait.", extensions={"status_code": 409})
            result = await handle.result() 
            user_id=result['userId']
            return User_details(
                userId=user_id,
                firstname=user_data.firstname,
                lastname=user_data.lastname,
                email=user_data.email,
                mobileNumber=user_data.mobileNumber,
                idProof=user_data.idProof,
                profilephoto=user_data.profilephoto,
                hobbies=user_data.hobbies,
                addressInfo=user_data.addressInfo,
                language=user_data.language,
                roles=user_data.roles
            )
            # return ResponseMessage(
            #     status="success",
            #     message=f"User created with ID: {result['userId']}"
            # )
        else:
            try:
                #inject dependenceny for db
                db: AsyncSession = info.context["db"]
                #validate fields with pydantic schemas
                validated = CreateUser(**data.__dict__)
                async with db.begin():
                    if validated.password != validated.password1:
                        raise GraphQLError('enter correct password',extensions={"status_code":400})
                    hash_password=password_context.hash(validated.password)
                    emails_exists_res=await db.execute(select(CustomUser).where(CustomUser.email==validated.email))
                    email_exists=emails_exists_res.scalar_one_or_none()
                    if email_exists:
                        raise GraphQLError('email already exists',extensions={"status_code":400})
                    
                    users=CustomUser(email=validated.email,mobile_number=validated.mobileNumber,password=hash_password)
                    db.add(users)
                    await db.flush()

                    profile=UserPersonalProfile(firstname=validated.firstname,lastname=validated.lastname,user_id=users.id,created_by=str(users.id))
                    db.add(profile)

                    role_res=await db.execute(select(RoleMaster).where(RoleMaster.name.in_(validated.roles)))
                    if not role_res:
                        raise HTTPException(status_code=400,detail='role not found')
                    roles=role_res.scalars()
                    for role in roles:
                        db.add(RoleMapping(user_id=users.id,role_id=role.id))
                    if data.language:
                        lang_res=await db.execute(select(Language).where(Language.name.in_(validated.language)))
                        language=lang_res.scalars()
                        for lang in language:
                            await db.execute(insert(language_users).values(user_id=users.id,language_id=lang.id))
                    await db.refresh(users)
                    await db.refresh(profile)
                    return User_details(
                    userId=users.id,
                    firstname=profile.firstname,
                    lastname=profile.lastname,
                    email=users.email,
                    mobileNumber=users.mobile_number,
                    idProof=users.id_proof,
                    profilephoto=profile.profilephoto,
                    hobbies=profile.hobbies,
                    addressInfo=profile.address_info,
                    language=validated.language,
                    roles=validated.roles
            )
            except GraphQLError as gql_error:
                raise gql_error  
            except Exception as e:
                await db.rollback()
                raise GraphQLError(f"Something went wrong :{str(e)}")
