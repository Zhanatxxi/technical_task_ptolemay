from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from technical_project.apps.departament.schemas import DepartmentSchema
from technical_project.apps.departament.services import select_department
from technical_project.db.deps import get_db_session

departament_route = APIRouter()


@departament_route.get("/", response_model=list[DepartmentSchema | None])
async def get_departments(session: AsyncSession = Depends(get_db_session)):
    departments = await select_department(session)
    return departments

