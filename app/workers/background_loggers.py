import time
from datetime import datetime

def log_inference_to_db(user_id: int, input_text: str, prediction: str):
    """
    Yeh function background mein chalega. Abhi hum sirf terminal mein print kar rahe hain
    (to simulate database saving lag). Aage chalkar hum isme actual DB logic likhenge.
    """
    print(f"\n🕒 [Background Task Started] at {datetime.now().strftime('%H:%M:%S')}")
    
    # Hum jaan-boojh kar 5 second ka delay daal rahe hain ye feel karne ke liye
    # ki agar database slow bhi ho, toh humari API slow nahi hogi.
    time.sleep(5)
    
    print(f"✅ [Background Task Finished] Logged -> User: {user_id} | Text: '{input_text}' | AI says: {prediction}\n")