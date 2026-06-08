from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from app.core.config import settings

# 1. Cloud Database se connection engine banana
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Database Table ka Blueprint (Schema) banana
class InferenceLog(Base):
    __tablename__ = "inference_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    prediction = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    model_version = Column(Integer, nullable=False)
    latency_ms = Column(Float, nullable=False)
    cached = Column(String, default="false")
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    """API endpoints ke liye database session provide karta hai."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CONNECTION TEST ---
if __name__ == "__main__":
    print("⏳ Connecting to Neon Cloud PostgreSQL...")
    try:
        # Ye command automatically database mein 'inference_logs' table bana degi
        Base.metadata.create_all(bind=engine)
        print("✅ Database connection successful aur table create ho gayi!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")