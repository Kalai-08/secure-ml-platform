from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.audit import log_event
from app.core.database import get_db
from app.deps import require_roles, get_current_user
from app.models import Role, User
from app.schemas import UserOut

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_roles(Role.admin))]
)

@router.get("/users", response_model=list[UserOut])
def list_users(
    request: Request,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    log_event(
        db,
        "admin_list_users",
        request=request,
        user_id=current.id,
        email=current.email
    )
    return db.scalars(select(User).order_by(User.id)).all()