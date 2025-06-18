import strawberry

from src.schemas.user_schema import CreateUser
from .types import Create_role,Get_role,Create_user,ResponseMessage,Create_Lang,GetLang
from ...models.rolemaster import RoleMaster
from ...models.customuser import CustomUser
from ...models.rolemapping import RoleMapping
from ... models.user_profile import UserPersonalProfile
from ...models.language import Language,language_users
from ...dependency import SessionDeps
from sqlalchemy import insert, select
from fastapi import HTTPException,status
from ...utils import password_context
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.exceptions import GraphQLError
@strawberry.type
class Mutations():
    @strawberry.mutation
    async def Createrole(self,info:Info,data:Create_role)->Get_role:
        db: AsyncSession = info.context["db"]
        results=await db.execute(select(RoleMaster).where(RoleMaster.name==data.name))
        role_exists=results.scalar()
        if role_exists:
            raise HTTPException(status_code=400,detail='role already exists')
        roles=RoleMaster(name=data.name,desc=data.desc)
        db.add(roles)
        await db.commit()
        await db.refresh(roles)
        return roles
    
    @strawberry.mutation
    async def Createuser(self,info:Info,data:Create_user)->ResponseMessage:

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
                
                users=CustomUser(email=validated.email,mobile_number=validated.mobile_number,password=hash_password)
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

                lang_res=await db.execute(select(Language).where(Language.name.in_(validated.language)))
                language=lang_res.scalars()
                for lang in language:
                    await db.execute(insert(language_users).values(user_id=users.id,language_id=lang.id))
                await db.refresh(users)
                await db.refresh(profile)
                return ResponseMessage(status='success',message='user created successfully')     
        except GraphQLError as gql_error:
            #  Preserve the actual GraphQL error
            raise gql_error  
        except Exception as e:
            await db.rollback()
            raise GraphQLError(f"Something went wrong :{str(e)}")

    @strawberry.mutation
    async def CreateLanguage(self,info:Info,data:Create_Lang)->GetLang:
        db:AsyncSession=info.context["db"]
        lang=Language(name=data.name,created_by=str(1))
        db.add(lang)
        await db.commit()
        await db.refresh(lang)
        return lang
    