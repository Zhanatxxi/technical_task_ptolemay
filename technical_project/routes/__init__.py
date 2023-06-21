from fastapi import APIRouter

from technical_project.apps.auth.api import auth_routers
from technical_project.apps.departament.api import departament_route
from technical_project.apps.employee.api import employee_route

api_v1 = APIRouter()

api_v1.include_router(auth_routers, prefix="/auth", tags=["Auth"])
api_v1.include_router(employee_route, prefix="/employee", tags=["Employee"])
api_v1.include_router(departament_route, prefix="/departament", tags=["Departament"])
