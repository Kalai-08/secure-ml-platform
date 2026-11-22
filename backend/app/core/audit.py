from fastapi import Request
from sqlalchemy.orm import Session

from app.models import AuditLog

def log_event(
    db: Session,
    event: str,
    *,
    request: Request | None = None,
    user_id: int | None = None,
    email: str | None = None,
    success: bool = True,
    detail: str | None = None
) -> None:
    ip = request.client.host if request and request.client else None
    db.add(
        AuditLog(
            event=event,
            user_id=user_id,
            email=(email or "")[:320] or None,
            ip=ip,
            success=success,
            detail=detail
        )
    )
    db.commit()