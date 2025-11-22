from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models import user
from app.models import role
from app.models import permission
from app.models import user_role
from app.models import role_permission

from app.models.doctor import Doctor
from app.models.nurse import Nurse
from app.models.staff import Staff