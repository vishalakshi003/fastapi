from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from fastapi import APIRouter,Depends, HTTPException,Form
from sqlalchemy import select

from src.dependency import CurrentUserDeps, SessionDeps
from..schemas.user_schema import CreateUser, LoginRequest,UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.database import async_get_db
from ..models.customuser import CustomUser
from ..models.user_profile import UserPersonalProfile
from ..models.rolemaster import RoleMaster
from ..models.rolemapping import RoleMapping
from src.utils import fetch_current_user, generate_access_token, password_context
user_router=APIRouter()

@user_router.post('/create/user')
async def create_user(user:CreateUser,db:SessionDeps)-> dict:
    try:
        async with db.begin():
            new_user=CustomUser(
                email=user.email,
                mobile_number=user.mobile_number,
                password=password_context.hash(user.password),
                id_proof=user.id_proof        
            )
            db.add(new_user)
            await db.flush()# to push data to get user id

            user_profile=UserPersonalProfile(
                user_id=new_user.id,
                firstname=user.firstname,
                middlename=user.middlename,
                lastname=user.lastname,
                profilephoto=user.profilephoto,
                hobbies=user.hobbies,
                address_info=user.address_info,
                created_by=str(new_user.id)
            )
            db.add(user_profile)
            result=await db.execute(select(RoleMaster).where(RoleMaster.name.in_(user.roles)))
            if not result:
                raise HTTPException(status_code=404,detail="role not found")
            roles=result.scalars()
            for role in roles:
                db.add(RoleMapping(user_id=new_user.id,role_id=role.id))
        await db.refresh(new_user)
        await db.refresh(user_profile)
        return {"status": "success", "message": "Registration completed", "user_id": new_user.id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@user_router.post('/login')
async def login_user(request:LoginRequest,db:SessionDeps):
    results=await db.execute(select(CustomUser).where(CustomUser.mobile_number==request.mobilenumber))
    users=results.scalar()
    if not users or not password_context.verify(request.password,users.password):
        raise HTTPException(status_code=404,detail='mobile no or password is invalid')
    token = generate_access_token(data={
            "user":{
                    "id":users.id,
                    "email":users.email,
                },})
    return token
    
@user_router.post('/oauth/login')
async def login_form(request_form: Annotated[OAuth2PasswordRequestForm,Depends()],db:SessionDeps):
    results=await db.execute(select(CustomUser).where(CustomUser.mobile_number==request_form.username))
    users=results.scalar()
    if not users or not password_context.verify(request_form.password,users.password):
        raise HTTPException(status_code=404,detail='mobile no or password is invalid')
    token = generate_access_token(data={
            "user":{
                    "id":users.id,
                    "email":users.email,
                },})
    return token
@user_router.post("/dashboad")
async def dashboard(current_user:CurrentUserDeps):
    print(current_user)
    return {"message": f"hello {current_user['user']['email']}!!!!"}



