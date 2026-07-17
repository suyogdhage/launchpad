from schemas.user_schema import CreateUser
from models.user_model import Users
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies.auth import Authentication
from models.role_model import Role
from sqlalchemy import select
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:
    @staticmethod
    async def register_user(user:CreateUser,db:AsyncSession):
        try:
            user=Users(name=user.name,email=user.email,password=Authentication.hash_password(user.password))
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def get_user_by_email(email:str,db:AsyncSession):
        try:
            result=await db.execute(select(Users).where(Users.email==email))
            return result.scalars().one_or_none()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

    @staticmethod
    async def get_all_user(db:AsyncSession):
        try:
            result=await db.execute(select(Users))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
    
    @staticmethod
    async def get_user_by_id(id:UUID,db:AsyncSession):
        try:
            result=await db.execute(select(Users).where(Users.id==id))
            return result.scalars().one_or_none()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        
    @staticmethod
    async def assign_manager(user:Users,manager_id:UUID,db:AsyncSession):
        try:
            user.assigned_to=manager_id
            await db.commit()
            return {f"{user.email} assigned to {manager_id}"}
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

            
    


        

