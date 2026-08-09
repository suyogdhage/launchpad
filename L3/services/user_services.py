from repository.user_repo import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user_schema import CreateUser,UserLogin
from fastapi import HTTPException,status
from dependencies.auth import Authentication
from dependencies.loggers import logger
from dependencies.email_service import email_service
from dependencies.s3 import UploadService
from dependencies.web_sockets import manager
from repository.dashboard_repo import DashboardRepository
from models.user_role import UserRole
from uuid import UUID
from config import settings


class UserServices:
    @staticmethod
    async def register_user(user: CreateUser, db: AsyncSession):
        existing = await UserRepository.get_user_by_email(user.email, db)

        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists")

        created_user = await UserRepository.register_user(user, db)
        logger.info(f"User created: {created_user.email}")
        email_service.send_email(
            to_email=created_user.email,
            subject="Welcome to Launchpad",
            html_body=f"""
            Hi {created_user.name},

            Welcome to Launchpad!

            Your account has been created successfully. Use the credentials below to sign in.

            <p><b>Your login details:</b></p>
            <ul>
                <li><b>Email:</b> {created_user.email}</li>
                <li><b>Password:</b> {user.password}</li>
            </ul>

            <p>Click here to sign in: <a href="{settings.FRONTEND_URL}/login">{settings.FRONTEND_URL}/login</a></p>
            """)
        return created_user
    
    @staticmethod
    async def login_user(data:UserLogin,db):
        user=await UserRepository.get_user_by_email(data.email,db)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User not exist")
        if not Authentication.verify_hash(data.password,user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Incorrect email or password")
        logger.info("Creating token")
        token=Authentication.create_access_token({"id":str(user.id),"role":user.role_name.value if isinstance(user.role_name, UserRole) else user.role_name})
        return {"token":token}
    
    @staticmethod
    async def get_all_user(db:AsyncSession):
        return await UserRepository.get_all_user(db)
    
    @staticmethod
    async def assign_manager(user_id:UUID,manager_id:UUID,db:AsyncSession):
        user=await UserRepository.get_user_by_id(user_id,db)
        manager=await UserRepository.get_user_by_id(manager_id,db)
        if manager.role_name != UserRole.MANAGER:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User you are assigning to is not manager")
        return await UserRepository.assign_manager(user,manager_id,db)

    @staticmethod
    async def get_team_members(manager_id: UUID, db: AsyncSession):
        return await UserRepository.get_team_members(manager_id, db)

    @staticmethod
    async def delete_user(user_id: UUID, current_user: dict, db: AsyncSession):
        if UUID(current_user["id"]) == user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot delete your own account")

        target = await UserRepository.get_user_by_id(user_id, db)
        if not target:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if target.role_name == UserRole.SUPERADMIN:
            superadmin_count = await UserRepository.count_users_with_role(UserRole.SUPERADMIN, db)
            if superadmin_count <= 1:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete the last superadmin")

        file_paths = await UserRepository.delete_user_with_data(user_id, db)
        logger.info(f"User deleted: {target.email} ({user_id})")

        for file_path in file_paths:
            try:
                UploadService.delete_file(file_path)
            except Exception as e:
                logger.warning(f"Failed to delete B2 file {file_path}: {e}")

        try:
            stats = await DashboardRepository.get_stats(db)
            await manager.broadcast(stats)
        except Exception as e:
            logger.warning(f"Failed to broadcast dashboard stats: {e}")

        return {"message": f"User {target.email} deleted successfully"}