import pandas as pd
from predict_logic import run_prediction_layer
from send_action import send_email, llm, prompt

def run_autonomous_loop():
    print("Starting autonomous agent")

    # 1. Predict
    run_prediction_layer()
    
    # 2. Data ingestion
    df = pd.read_csv("predicted_customers.csv")
    targets = df[df['anomaly_status'] != "Normal"]
    
    if targets.empty:
        print("No issues detected today.")
        return

    print(f"Found {len(targets)} anomalies. Starting Decision/Action phase\n")

    # 3. Decide and act
    for _, row in targets.iterrows():
        target_email = row['email'] 
        
        print(f"Processing agent decision for: {target_email}")
        
        chain = prompt | llm
        email_body = chain.invoke({
            "customer_id": row['customer_id'],
            "customer_profile": row['customer_profile'],
            "anomaly_status": row['anomaly_status'],
            "feedback_text": row['feedback_text'],
            "people_count": row['people_count'],
            "actual_daily_consumption": row['actual_daily_consumption']
        })

        subject = f"Supply Update: {row['anomaly_status']}"
        success = send_email(subject, email_body, target_email)
        
        if success:
            print(f"Email successfully sent to {target_email}\n")

if __name__ == "__main__":
    run_autonomous_loop()