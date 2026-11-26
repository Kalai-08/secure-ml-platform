from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog

WINDOW_MINUTES = 15
MAX_FAILURES_PER_EMAIL = 5
MAX_FAILURES_PER_IP = 20

def _failed_logins(db: Session, *conditions) -> int:
    since = datetime.now(timezone.utc) - timedelta(minutes=WINDOW_MINUTES)
    stmt = (
        select(func.count())
        .select_from(AuditLog)
        .where(
            AuditLog.event == "login",
            AuditLog.success.is_(False),
            AuditLog.created_at >= since,
            *conditions
        )
    )
    return db.scalar(stmt) or 0

def login_blocked(db: Session, email: str, ip:str | None) -> bool:
    if _failed_logins(db, AuditLog.email == email) >= MAX_FAILURES_PER_EMAIL:
        return True
    if ip and _failed_logins(db, AuditLog.ip == ip) >= MAX_FAILURES_PER_IP:
        return True
    return False
