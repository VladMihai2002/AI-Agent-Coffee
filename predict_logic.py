import pandas as pd
from sklearn.cluster import KMeans
from datetime import datetime

INPUT_FILE = "customers.csv"
OUTPUT_FILE = "predicted_customers.csv"
CURRENT_DATE = datetime(2026, 4, 6)

def run_prediction_layer():
    df = pd.read_csv(INPUT_FILE)
    print("Data ingested successfully for prediction...")

    def identify_anomaly(row):
        if row['actual_daily_consumption'] > (row['theoretical_daily_consumption'] * 2):
            return "Consumption Surge"
        
        last_order = pd.to_datetime(row['last_order_date'])
        days_since_order = (CURRENT_DATE - last_order).days
        if days_since_order > 30:
            return "Churn Risk"
        
        return "Normal"

    df['anomaly_status'] = df.apply(identify_anomaly, axis=1)

   # Clustering
    X = df[['people_count', 'actual_daily_consumption']]
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['cluster_id'] = kmeans.fit_predict(X)

    # Mean consumption for each cluster
    cluster_means = df.groupby('cluster_id')['actual_daily_consumption'].mean().sort_values().index
    
    mapping = {
        cluster_means[0]: "Residential/Small",
        cluster_means[1]: "Medium Enterprise",
        cluster_means[2]: "Large Office"
    }
    
    df['customer_profile'] = df['cluster_id'].map(mapping)

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Prediction layer finished. Results saved to {OUTPUT_FILE}")
    
    print("\nDetected Anomalies:")
    print(df[df['anomaly_status'] != "Normal"][['customer_id', 'anomaly_status']])

if __name__ == "__main__":
    run_prediction_layer()