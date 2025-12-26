import bcrypt
import hashlib
import re
from fastapi import HTTPException
from app.storage.db import users_collection
import secrets
from datetime import datetime, timedelta, timezone

import secrets
from app.services.email_service import send_reset_email
from app.config import FRONTEND_RESET_URL


# --------------------------------------------------
# Password Validation Rules
# --------------------------------------------------
def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long"
        )

    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase letter"
        )

    if not re.search(r"[0-9]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one number"
        )

    if not re.search(r"[!@#$%^&*]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one special character"
        )


# --------------------------------------------------
# Normalize Password (Fix bcrypt 72-byte limit)
# SHA-256 → bcrypt
# --------------------------------------------------
def _normalize_password(password: str) -> bytes:
    """
    Hash password with SHA-256 first,
    then bcrypt → avoids 72-byte bcrypt limit
    """
    return hashlib.sha256(password.encode("utf-8")).digest()


# --------------------------------------------------
# Create User
# --------------------------------------------------
def create_user(username: str, password: str, role: str) -> bool:
    # Check if user already exists
    if users_collection.find_one({"username": username}):
        return False

    # Validate password strength
    validate_password(password)

    # Hash password securely
    hashed_password = bcrypt.hashpw(
        _normalize_password(password),
        bcrypt.gensalt()
    )

    # Store user
    users_collection.insert_one({
        "username": username,
        "password": hashed_password,
        "role": role
    })

    return True


# --------------------------------------------------
# Get User
# --------------------------------------------------
def get_user(username: str):
    return users_collection.find_one({"username": username})


# --------------------------------------------------
# Verify Password
# --------------------------------------------------
def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(
        _normalize_password(password),
        hashed
    )
# --------------------------------------------------
# Generate Reset Token
# --------------------------------------------------

def generate_reset_token(username: str) -> str:
    user = get_user(username)
    if not user:
        raise HTTPException(404, "User not found")

    raw_token = secrets.token_urlsafe(32)
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

    users_collection.update_one(
        {"username": username},
        {"$set": {
            "reset_token": hashed_token,
            "reset_token_expiry": datetime.now(timezone.utc) + timedelta(minutes=15)
        }}
    )

    # In real app → email this token
    return raw_token
# --------------------------------------------------
# Reset Password
# --------------------------------------------------

def reset_password(token: str, new_password: str):
    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    user = users_collection.find_one({
        "reset_token": hashed_token,
        "reset_token_expiry": {"$gt": datetime.now(timezone.utc)}
    })

    if not user:
        raise HTTPException(400, "Invalid or expired reset token")

    validate_password(new_password)

    new_hashed_password = bcrypt.hashpw(
        _normalize_password(new_password),
        bcrypt.gensalt()
    )

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "password": new_hashed_password
        },
         "$unset": {
            "reset_token": "",
            "reset_token_expiry": ""
         }}
    )

    return True
# --------------------------------------------------
# Request Password Reset Email
# --------------------------------------------------
'''def request_password_reset(email: str):
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(404, "User not found")

    raw_token = secrets.token_urlsafe(32)
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "reset_token": hashed_token,
            "reset_token_expiry":datetime.now(timezone.utc) + timedelta(minutes=15)
        }}
    )

    reset_link = f"{FRONTEND_RESET_URL}?token={raw_token}"
    send_reset_email(email, reset_link)

    return True'''
# --------------------------------------------------
# Generate token only (without email)
# For Swagger/manual usage
# --------------------------------------------------
def request_password_reset_token(username_or_email: str) -> str:
    """
    Generates a reset token and returns it instead of sending email.
    Useful for testing through Swagger.
    """
    user = users_collection.find_one({
        "$or": [{"username": username_or_email}, {"email": username_or_email}]
    })

    if not user:
        raise HTTPException(404, "User not found")

    raw_token = secrets.token_urlsafe(32)
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {
            "reset_token": hashed_token,
            "reset_token_expiry":datetime.now(timezone.utc)+ timedelta(minutes=15)
        }}
    )

    return raw_token     # return raw token (for swagger testing)

# --------------------------------------------------
# Confirm Password Reset
# --------------------------------------------------
def confirm_password_reset(token: str, new_password: str):
    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    user = users_collection.find_one({
        "reset_token": hashed_token,
        "reset_token_expiry": {"$gt": datetime.utcnow()}
    })

    if not user:
        raise HTTPException(400, "Invalid or expired token")

    validate_password(new_password)

    hashed_pw = bcrypt.hashpw(
        _normalize_password(new_password),
        bcrypt.gensalt()
    )

    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"password": hashed_pw},
         "$unset": {"reset_token": "", "reset_token_expiry": ""}}
    )
