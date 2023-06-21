from sqladmin import ModelView

from technical_project.apps.employee.models import Employee


class EmployeeAdmin(ModelView, model=Employee):
    name = "Employee"
    name_plural = "Employees"

    column_list = [
        Employee.id,
        Employee.surname,
        Employee.surname,
        Employee.age,
        Employee.position,
        Employee.salary,
        Employee.date,
        Employee.departament,
    ]

