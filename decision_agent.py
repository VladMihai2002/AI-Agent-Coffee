import pandas as pd
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

INPUT_FILE = "predicted_customers.csv"
MODEL_NAME = "llama3.1:8b-instruct-q4_K_M"

llm = OllamaLLM(model=MODEL_NAME)

template = """
You are an AI Business Agent for a smart coffee distribution company.
Your goal is to analyze customer data and decide the best action to take.

CUSTOMER DATA:
- ID: {customer_id}
- Profile: {customer_profile}
- Anomaly Status: {anomaly_status}
- Feedback: {feedback_text}
- People Count: {people_count}
- Actual Consumption: {actual_daily_consumption}g/day

DECISION RULES:
1. If Status is 'Consumption Surge', suggest a bulk package or ask if the team grew.
2. If Status is 'Churn Risk', offer a loyalty discount and ask for feedback.
3. Use the 'Feedback' to personalize the tone.

STRICT OUTPUT RULES:
1. Write ONLY the email body.
2. DO NOT include a 'Subject' line.
3. DO NOT include 'Action Plan', 'Decision', or any introductory remarks.
4. DO NOT explain your thoughts.
5. Max 3 sentences.
6. Start with 'Dear...' and end with 'Best regards, AI Team'.

EMAIL BODY:
"""

prompt = PromptTemplate(input_variables=["customer_id", "customer_profile", "anomaly_status", "feedback_text", "people_count", "actual_daily_consumption"], template=template)

def run_decision_layer():
    df = pd.read_csv(INPUT_FILE)
    
    # Only anomalies to save time
    anomalies = df[df['anomaly_status'] != "Normal"]
    
    print(f"Agent is deciding actions for {len(anomalies)} anomalies.\n")

    for index, row in anomalies.iterrows():
        # Decision
        chain = prompt | llm
        response = chain.invoke({
            "customer_id": row['customer_id'],
            "customer_profile": row['customer_profile'],
            "anomaly_status": row['anomaly_status'],
            "feedback_text": row['feedback_text'],
            "people_count": row['people_count'],
            "actual_daily_consumption": row['actual_daily_consumption']
        })
        
        print(f"Decision for {row['customer_id']} ")
        print(response)
        print("\n")

if __name__ == "__main__":
    run_decision_layer()