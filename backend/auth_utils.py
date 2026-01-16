import os
from pathlib import Path
import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv

# Load environment variables from multiple possible locations
env_paths = [
    Path(__file__).parent / ".env.local",  # src/backend/.env.local
    Path(__file__).parent.parent.parent / ".env",  # project root .env
    ".env.local",  # current directory
]

for env_path in env_paths:
    if Path(env_path).exists():
        load_dotenv(env_path, override=True)
        break

# Shared secret between Frontend and Backend
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
if not BETTER_AUTH_SECRET:
    # Log a warning if the secret is not set
    import warnings
    warnings.warn("BETTER_AUTH_SECRET environment variable is not set. Using default secret. This is insecure for production!")
    BETTER_AUTH_SECRET = "default_secret_change_me"

security = HTTPBearer(
    scheme_name="bearerAuth",
    description="Enter **Admin token** for Admin or use **Guest token**=`guest_token` for guest access. The lock icon will turn Authorized if passed."
)

def verify_jwt(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Verifies the JWT token from Better Auth.
    Expects 'Authorization: Bearer <token>'
    Allows 'guest_token' for public demo access.
    """
    token = credentials.credentials
    
    # Guest & Admin Access Bypass for Hackathon Demo
    if token == "guest_token":
        return "guest_user"
    if token == "admin_token":
        return "admin"

    try:
        # Better Auth usually issues RS256 or HS256.
        # For simplicity in this Hackathon project, we assume the shared secret HS256 flow.
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"],
            # Better Auth tokens might have specific audience settings,
            # we keep it flexible for now or skip if verification is purely signature based.
            options={"verify_aud": False}
        )
        user_id = payload.get("sub") # 'sub' is standard for user ID in JWTs
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user ID ('sub')",
            )
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token signature is invalid",
        )
    except jwt.InvalidTokenError as e:
        # Catch other token errors that aren't specifically expired
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
        )
    except Exception as e:
        # Catch any other unexpected errors during JWT decoding
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}",
        )
