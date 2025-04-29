from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ✅ SQLite database URL
DATABASE_URL = "sqlite:///./test.db"

# ✅ Create engine with special connect_args for SQLite
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# ✅ Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
