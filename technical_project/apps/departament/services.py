from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from technical_project.apps.departament.models import Departament
from technical_project.apps.employee.models import Employee


async def select_department(session: AsyncSession):
    stmt = select(
        Departament,
        func.count(Employee.id).label('employee_count'),
        func.sum(Employee.salary).label('total_salary')
    ).join(Departament.employees).group_by(Departament)

    result = await session.execute(stmt)
    departments = result.fetchall()

    department_list = []
    for department, employee_count, total_salary in departments:
        department_data = {
            'id': department.id,
            'title': department.title,
            'date': department.date,
            'employee_count': employee_count,
            'total_salary': total_salary
        }
        department_list.append(department_data)

    return department_list

