from app.core.database import SessionLocal, InferenceLog

def log_inference_to_db(
    user_id: int,
    prediction: str,
    confidence: float,
    model_version: int,
    latency_ms: float,
    cached: bool = False
):
    """Ye function background mein chalega aur Cloud DB mein data save karega."""
    db = SessionLocal()
    try:
        # 1. RDBMS table ke liye naya record (row) banaya
        log_entry = InferenceLog(
            user_id=user_id,
            prediction=prediction,
            confidence=confidence,
            model_version=model_version,
            latency_ms=latency_ms,
            cached=str(cached).lower()
        )
        
        # 2. Record ko database mein Add aur Commit kiya
        db.add(log_entry)
        db.commit()
        print(f"✅ [DB Logged] User: {user_id} | Pred: {prediction} | Latency: {latency_ms:.2f}ms")
        
    except Exception as e:
        print(f"❌ DB logging error: {e}")
        db.rollback() # Agar koi error aayi toh RDBMS transaction rollback kar do
    finally:
        db.close() # Connection wapas pool mein daal do