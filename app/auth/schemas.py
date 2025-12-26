from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    username: str
    password: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Password reset models
class PasswordResetRequest(BaseModel):  # for token generation manually
    username: str

class PasswordResetEmailRequest(BaseModel):  # for email sending
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
