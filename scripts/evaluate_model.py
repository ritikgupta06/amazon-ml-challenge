import pandas as pd
from sklearn.metrics import classification_report
import joblib

# File paths
features_file = 'data/features.csv'
model_file = 'models/model.pkl'

# Load features and labels
df = pd.read_csv(features_file)
X = df[['mean_blue', 'mean_green', 'mean_red', 'std_blue', 'std_green', 'std_red']]
y = df['filename'].apply(lambda x: int(x.split('_')[1].split('.')[0]))  # Example: Extract group_id from filename

# Load model
model = joblib.load(model_file)

# Predict
y_pred = model.predict(X)

# Evaluation
report = classification_report(y, y_pred)
print(f"Model evaluation:\n{report}")

# Save evaluation report
with open('data/results/model_performance.txt', 'w') as f:
    f.write(report)
