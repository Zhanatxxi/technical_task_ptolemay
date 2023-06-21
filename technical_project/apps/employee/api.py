from fastapi import APIRouter, Depends, Path, Query

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate

from apps.auth.services import require_user
from technical_project.apps.employee.services import insert_employee, select_employees, delete_employee_by_id
from technical_project.apps.employee.schemas import EmployeeCreateSchema, EmployeeOutDB
from technical_project.db.deps import get_db_session

employee_route = APIRouter()


@employee_route.post("/", response_model=EmployeeOutDB)
async def create_employee(
    employee: EmployeeCreateSchema,
    session: AsyncSession = Depends(get_db_session),
    user_id: str = Depends(require_user)
):
    employee = await insert_employee(session, employee)
    return employee


@employee_route.get("/", response_model=Page[EmployeeOutDB | None])
async def get_employee(
    surname: str | None = Query(None),
    department_id: int | None = Query(None),
    session: AsyncSession = Depends(get_db_session),
    user_id: str = Depends(require_user)
):
    employees = await select_employees(session, surname, department_id)
    return paginate(employees)


@employee_route.delete("/{employee_id}")
async def delete_employee(
    session: AsyncSession = Depends(get_db_session),
    employee_id: int = Path(gt=0),
    user_id: str = Depends(require_user)
):
    await delete_employee_by_id(session, employee_id)
    return "delete employee"
