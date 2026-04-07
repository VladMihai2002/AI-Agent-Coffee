import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decision_agent import llm, prompt 
 
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "sender@example.com"
SENDER_PASSWORD = "16 letters"

def send_email(subject, body, to_email):
    """Sends a personalized email to a specific customer destination."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() 
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")
        return False

def run_action_layer():
    """Autonomous execution layer: Predict -> Decide -> Act."""
    df = pd.read_csv("predicted_customers.csv")
    
    anomalies = df[df['anomaly_status'] != "Normal"]

    print(f"AI Agent: Executing actions for {len(anomalies)} customers\n")

    for index, row in anomalies.iterrows():
        # 1. Decide
        chain = prompt | llm
        decision_text = chain.invoke({
            "customer_id": row['customer_id'],
            "customer_profile": row['customer_profile'],
            "anomaly_status": row['anomaly_status'],
            "feedback_text": row['feedback_text'],
            "people_count": row['people_count'],
            "actual_daily_consumption": row['actual_daily_consumption']
        })

        # 2. Act
        customer_destination = row['email'] 
        subject = f"Coffee Supply Update for {row['customer_id']}"
        
        success = send_email(subject, decision_text, customer_destination)
        
        if success:
            print(f"Autonomous email sent to {customer_destination} ({row['anomaly_status']})")
        else:
            print(f"Could not reach {customer_destination}")

if __name__ == "__main__":
    run_action_layer()