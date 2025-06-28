from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
import secrets
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import httpx

from .. import schemas
from ..database import models
from ..dependencies import get_db
from ..security import (create_access_token, get_password_hash, verify_password, 
                      ACCESS_TOKEN_EXPIRE_MINUTES, GOOGLE_CLIENT_ID, 
                      GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI)
from ..main import limiter

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
@limiter.limit("5/minute")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """Logs in a user and returns a JWT access token."""
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or user.provider != 'local' or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/hour")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Creates a new user."""
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, 
        hashed_password=hashed_password,
        provider="local"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/auth/google", response_model=schemas.Token)
async def auth_google(auth_code: schemas.GoogleAuthCode, db: Session = Depends(get_db)):
    """Handles the Google OAuth2 callback."""
    token_url = "https://oauth2.googleapis.com/token"
    async with httpx.AsyncClient() as client:
        token_response = await client.post(token_url, data={
            "code": auth_code.code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        })
        token_data = token_response.json()
        if "error" in token_data:
            raise HTTPException(status_code=400, detail=f"Google login error: {token_data.get('error_description')}")

        userinfo_response = await client.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {token_data['access_token']}"})
        user_info = userinfo_response.json()
        user_email = user_info.get("email")

        if not user_email:
            raise HTTPException(status_code=400, detail="Email not available from Google account.")

        user = db.query(models.User).filter(models.User.username == user_email).first()
        if not user:
            user = models.User(username=user_email, provider="google")
            db.add(user)
            db.commit()
            db.refresh(user)
        elif user.provider != "google":
            raise HTTPException(status_code=400, detail="Account with this email already exists. Please log in with your password.")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/password-forgot", status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("5/minute")
async def request_password_reset(
    request: schemas.PasswordResetRequest, 
    db: Session = Depends(get_db)
):
    """Initiates a password reset request for a local user."""
    user = db.query(models.User).filter(models.User.username == request.email, models.User.provider == "local").first()
    if user:
        token = secrets.token_urlsafe(32)
        reset_token = models.PasswordResetToken(token=token, user_id=user.id)
        db.add(reset_token)
        db.commit()

        # --- Email Sending Logic ---
        # In a real application, you would use a background task to send this email.
        # This prevents the API from waiting on the email service.
        reset_url = f"http://localhost:8000/reset-password?token={token}"
        print(f"--- PASSWORD RESET ---")
        print(f"To: {user.username}")
        print(f"URL: {reset_url}")
        print(f"--------------------")
        # Example with fastapi-mail would be:
        # message = MessageSchema(...)
        # await fm.send_message(message)

    return {"message": "If an account with that email exists, a password reset link has been sent."}

@router.post("/password-reset", status_code=status.HTTP_200_OK)
def reset_password(request: schemas.PasswordReset, db: Session = Depends(get_db)):
    """Resets the user's password using a valid token."""
    token = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == request.token).first()

    if not token or token.used or token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token.")

    token.user.hashed_password = get_password_hash(request.new_password)
    token.used = True
    db.commit()
    return {"message": "Password has been reset successfully."}