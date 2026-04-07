Coffee Order Recovery Agent 
This is an AI-powered system. It follows the Predict -> Decide -> Act cycle to ensure business customers never run out of coffee.

What it does
Predict: Uses Machine Learning (K-Means) to profile customers and detects anomalies like consumption surges or churn risks.

Decide: Uses Llama 3.1 (8B) to analyze the data and the customer's feedback to create a personalized recovery plan.

Act: Automatically sends a professional email with a custom offer to the customer.

Tech Stack
Language: Python


AI/LLM: Ollama (Llama 3.1 8B), LangChain 

Machine Learning: Scikit-learn, Pandas

Backend: FastAPI (for the logic structure)

How to Run
Generate Data: python generate_data.py (Creates the initial customer list)

Predict: python predict_logic.py (Runs ML to find anomalies and profiles)

Decide & Act: python send_action.py (AI generates the email and sends it via SMTP)

Autonomous Workflow: python main.py — The main entry point that coordinates the entire cycle (Analysis, Filtering, and AI Generation) in a single run.
