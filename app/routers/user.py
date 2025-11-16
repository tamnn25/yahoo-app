from fastapi import APIRouter, HTTPException, Form
from app.database import get_connection
from app.schemas.user import FriendRequest
from passlib.context import CryptContext

router = APIRouter(prefix="/user", tags=["User"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MAX_BCRYPT_LENGTH = 72  # bcrypt max password length

# def hash_password(password: str) -> str:
#     """
#     Truncate the password if it's longer than 72 bytes and hash it.
#     """
#     safe_password = password[:MAX_BCRYPT_LENGTH]
#     return pwd_context.hash(safe_password)

import bcrypt

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode()

@router.post("/register")
def register(
    username: str = Form(..., min_length=3, max_length=50),
    password: str = Form(..., min_length=8, max_length=64)
    ):
    hashed_password = hash_password(password)

    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )
        conn.commit()
        return {"msg": "User created successfully"}
    except Exception as e:
        # Catch unique constraint / duplicate username errors
        return {"msg": f"Failed to create user: {str(e)}"}
    finally:
        conn.close()

# List all users
@router.get("/")
def list_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM users")
    users = [dict(row) for row in cur.fetchall()]
    conn.close()
    return users

# Add friend
@router.post("/{username}/add_friend")
def add_friend(username: str, req: FriendRequest):
    conn = get_connection()
    cur = conn.cursor()

    # Get user IDs
    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cur.execute("SELECT id FROM users WHERE username = ?", (req.username,))
    friend = cur.fetchone()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    try:
        cur.execute("INSERT INTO friends (user_id, friend_id) VALUES (?, ?)", (user["id"], friend["id"]))
        conn.commit()
    except:
        conn.close()
        raise HTTPException(status_code=400, detail="Already friends")

    conn.close()
    return {"message": f"{req.username} added as friend for {username}"}

# List friends
@router.get("/{username}/friends")
def list_friends(username: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cur.execute("""
    SELECT u.id, u.username FROM users u
    JOIN friends f ON u.id = f.friend_id
    WHERE f.user_id = ?
    """, (user["id"],))
    friends = [dict(row) for row in cur.fetchall()]
    conn.close()
    return friends
