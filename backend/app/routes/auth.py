from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.audit import log_event
from app.core.database import get_db
from app.core.security import create_access_token, verify_password, hash_password
from app.deps import get_current_user
from app.models import User
from app.schemas import Token, UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"]) #tags is used for grouping the endpoints in the documentation

_DUMMY_HASH = hash_password("dummy_password_for_testing")  # Used to mitigate timing attacks

@router.post("/register", response_model=UserOut, status_code = status.HTTP_201_CREATED)
def register(payload: UserCreate, request: Request, db: Session = Depends(get_db)):
    email = payload.email.lower()
    if db.scalar(select(User).where(User.email == email)):
        log_event(
            db,
            "register", 
            request=request, 
            email=email,
            success=False,
            detail="Email already registered"
        )
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(email=email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user) # It will refresh the user object with the data from the database, including the generated ID
    log_event(
        db,
        "register",
        request=request, # request means that we can get the IP address of the user from the request object
        user_id=user.id,
        email=email
    )
    return user

@router.post("/login", response_model=Token)
def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form.username.lower()
    user = db.scalar(select(User).where(User.email == email))
    password_hash = user.password_hash if user else _DUMMY_HASH  # Use dummy hash if user not found
    password_ok = verify_password(form.password, password_hash)
    if user is None or not password_ok or not user.is_active:
        reason=(
            "unknown email" if user is None
            else "bad password" if not password_ok
            else "inactive user"
        )

        log_event(
            db,
            "login",
            request=request,
            user_id=user.id if user else None,
            email=email,
            success=False,
            detail=reason
        )

        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    return Token(access_token=create_access_token(user.id))

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user