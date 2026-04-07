import pandas as pd
from datetime import datetime, timedelta
import random

NUM_CUSTOMERS = 10
OUTPUT_FILE = "customers.csv"

def generate_synthetic_data():
    customers = []
    current_date = datetime(2026, 4, 6) 

    for i in range(1, NUM_CUSTOMERS + 1):
        people_count = random.randint(2, 10)
        theoretical_daily_consumption = people_count * 30 
        
        actual_daily_consumption = theoretical_daily_consumption
        last_order_days_ago = random.randint(10, 20)
        grams_purchased = 1000
        feedback = "Good quality coffee."
        
        if i == 1: 
            people_count = 2
            theoretical_daily_consumption = 60 
            actual_daily_consumption = 300 
            last_order_days_ago = 3
            grams_purchased = 500
            feedback = "We are drinking so much of this new blend!"
            
        elif i == 2:
            last_order_days_ago = 40
            feedback = "Haven't had time to reorder."

        last_order_date = current_date - timedelta(days=last_order_days_ago)

        customers.append({
            "customer_id": f"CUST_{i:03d}",
            "email": f"client_{i}@example.com",
            "last_order_date": last_order_date.strftime("%Y-%m-%d"),
            "grams_purchased": grams_purchased,
            "people_count": people_count,
            "theoretical_daily_consumption": theoretical_daily_consumption,
            "actual_daily_consumption": actual_daily_consumption,
            "feedback_text": feedback,
            "loyalty_score": random.randint(1, 10)
        })

    df = pd.DataFrame(customers)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Successfully generated {OUTPUT_FILE} with explicit anomalies.")

if __name__ == "__main__":
    generate_synthetic_data()