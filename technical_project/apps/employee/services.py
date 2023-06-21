from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from technical_project.apps.employee.schemas import EmployeeCreateSchema
from technical_project.apps.employee.models import Employee


async def insert_employee(
    session: AsyncSession,
    employee: EmployeeCreateSchema
) -> Employee:
    employee = Employee(**employee.dict())
    session.add(employee)
    await session.commit()
    return employee


async def select_employees(
    session: AsyncSession,
    surname: str | None = None,
    department_id: int | None = None
):
    stmt = select(Employee)
    if surname:
        stmt = stmt.filter(Employee.surname.ilike(f"%{surname}%"))

    if department_id:
        stmt = stmt.filter(Employee.departament_id == department_id)

    employees = await session.scalars(stmt)
    return employees.all()


async def delete_employee_by_id(
    session: AsyncSession,
    employee_id: int
):
    stmt = delete(Employee).where(Employee.id == employee_id)
    await session.execute(stmt)
    await session.commit()


