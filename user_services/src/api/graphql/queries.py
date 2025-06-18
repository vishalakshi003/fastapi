import strawberry
from .types import Get_role,User_details,GetLang
from typing import Optional
from ...dependency import SessionDeps
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ...models.rolemaster import RoleMaster
from ...models.customuser import CustomUser
from ...models.rolemapping import RoleMapping
from ...models.language import Language
from strawberry.types import Info
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import json
@strawberry.type
class Query:
    @strawberry.field
    async def get_roles(self,info:Info,id:Optional[int]=None)-> List[Get_role]:
        db: AsyncSession = info.context["db"]
        if id:
            results=await db.execute(select(RoleMaster).where(RoleMaster.id==id))
        else:
            results=await db .execute(select(RoleMaster))
        roles=results.scalars().all()
        return roles
    
    
    @strawberry.field
    async def get_user_details(self,info:Info,id:Optional[int]=None)->List[User_details]:
        db:AsyncSession=info.context["db"]
        if id:
            results = await db.execute(select(CustomUser).options(selectinload(CustomUser.profile)).where((CustomUser.id == id) & (CustomUser.is_active == True)))
        
        else:
            results = await db.execute(select(CustomUser).options(selectinload(CustomUser.profile) ,selectinload(CustomUser.language)).where((CustomUser.is_active == True)))
        users=results.scalars().all()
        user_data=[]
        for user in users:
            role_res=await db.execute(select(RoleMaster.name).join(RoleMapping,RoleMapping.role_id==RoleMaster.id).where(RoleMapping.user_id==user.id))
            role_res=role_res.scalars()
            role_name=[]

            for role in role_res:
                role_name.append(role)

                
            user_languages = [
            GetLang(id=lang.id, name=lang.name) for lang in user.language
            ]

            user_data.append(User_details(
                user_id=user.id,
                firstname=user.profile.firstname,
                lastname=user.profile.lastname,
                email=user.email,
                mobile_number=user.mobile_number,
                id_proof=user.id_proof,
                profilephoto=user.profile.profilephoto,
                hobbies=user.profile.hobbies,
                address_info=user.profile.address_info,
                language=user_languages,
                roles=", ".join(role_name) if role_name else "consumer"
            ))
        return user_data

    @strawberry.field
    async def get_language(self,info:Info,id:Optional[int]=None)->List[GetLang]:
        db:AsyncSession=info.context["db"]
        if id:
            data=await db.execute(select(Language).where((Language.id==id)&(Language.is_active == True)))
        else:
            data=await db.execute(select(Language).where(Language.is_active == True))
        language=data.scalars().all()
        return language

