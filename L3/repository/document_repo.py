from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.document_schemas import DocumentCreate,DocUpdate,Status
from models.document_model import Document
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID

class DocumentRepository:
    @staticmethod
    async def create_doc(doc,db:AsyncSession):
        try:
            db.add(doc)
            await db.commit()
            await db.refresh(doc)
            return doc
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        
    @staticmethod
    async def aprove_doc(document:Document,db:AsyncSession):
        try:
            document.status="approved"
            await db.commit()
            return {"message":"Approved Successfully"}
        except SQLAlchemyError as e:
            await db.rollback()
            raise e    
        
    @staticmethod
    async def reject_doc(reason:str,document:Document,db:AsyncSession):
        try:
            document.status="rejected"
            document.rejection_reason=reason
            await db.commit()
            return {"message":f"Rejected due to {reason}"}
        except SQLAlchemyError as e:
            await db.rollback()
            raise e    
        
    @staticmethod
    async def get_by_id(document_id:UUID,db:AsyncSession):
        try:
            result=await db.execute(select(Document).where(Document.id==document_id))
            return result.scalars().one_or_none()
        except SQLAlchemyError as e:
            await db.rollback()
            raise e
        
    @staticmethod
    async def update_task(data:DocUpdate,document:Document,db:AsyncSession):
        try:
            if data.status==Status.approved:
                document.status=Status.approved
                await db.commit()
                return {"message":"Approved Successfully"}
            else:
                document.status=Status.rejected
                document.rejection_reason=data.reason
                await db.commit()
                return {"message":"Rejected Successfully"}
        except SQLAlchemyError as e:
            await db.rollback()
            raise e

            

