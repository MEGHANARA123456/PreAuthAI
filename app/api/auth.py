
from app.auth.jwt import create_access_token
from app.auth.schemas import SignupRequest, LoginRequest, TokenResponse, PasswordResetRequest, PasswordResetConfirm,PasswordResetEmailRequest
from app.auth.auth_services import create_user, get_user, verify_password,generate_reset_token, reset_password# [request_password_reset,confirm_password_reset]
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/api/auth", tags=["Auth"]) 

@router.post("/signup")
def signup(data: SignupRequest):
    success = create_user(
        username=data.username,
        password=data.password,
        role=data.role
    )

    if not success:
        raise HTTPException(status_code=400, detail="User already exists")

    return {"status": "User registered successfully"}


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)

    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user["username"],
        "role": user.get("role", "user")
    })

    return {"access_token": token, "token_type": "bearer"}

@router.post("/password-reset/request")
def request_password_reset(data: PasswordResetRequest):
    token = generate_reset_token(data.username)

    return {
        "message": "Password reset token generated",
        "reset_token": token  # demo purpose only
    }

@router.post("/password-reset/confirm")
def confirm_password_reset(data: PasswordResetConfirm):
    reset_password(data.token, data.new_password)
    return {"message": "Password updated successfully"}

#@router.post("/password-reset/email")
#def password_reset_email(data: PasswordResetEmailRequest):
    request_password_reset(data.email)
    return {"message": "Password reset email sent"}

#@router.post("/password-reset/confirm")
#def password_reset_confirm(data: PasswordResetConfirm):
    confirm_password_reset(data.token, data.new_password)
    return {"message": "Password reset successful"}
@router.post("/password-reset/token")
def generate_reset_token_api(data: PasswordResetRequest):
    token = generate_reset_token(data.username)
    return {"reset_token": token}

