import os
from pathlib import Path
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.pool import QueuePool

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

# Database URL should be in .env:
# DATABASE_URL=postgresql://user:pass@ep-hostname.region.aws.neon.tech/dbname?sslmode=require
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback for local development if Neon URL is not provided
    DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    poolclass=QueuePool,
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
