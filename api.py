from uvicorn import run
from fastapi import FastAPI
from sqladmin import Admin
from fastapi_pagination import add_pagination

from technical_project import routes
from technical_project.apps.departament.admin import DepartamentAdmin
from technical_project.apps.employee.admin import EmployeeAdmin
from technical_project.db.session import engine

api = FastAPI(
    title="Technical task"
)

api.include_router(routes.api_v1, prefix="/api/v1")

add_pagination(api)

admin = Admin(api, engine)
admin.add_view(EmployeeAdmin)
admin.add_view(DepartamentAdmin)


if __name__ == '__main__':
    run("api:api", reload=True, workers=2)
