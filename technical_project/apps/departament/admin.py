from sqladmin import ModelView

from technical_project.apps.departament.models import Departament


class DepartamentAdmin(ModelView, model=Departament):
    name = "Departament"
    name_plural = "Departments"

    column_list = [
        Departament.id,
        Departament.title,
        Departament.employees,
        Departament.date
    ]

