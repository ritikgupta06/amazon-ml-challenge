import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# File paths
features_file = 'data/features.csv'
model_file = 'models/model.pkl'

# Load features and labels
df = pd.read_csv(features_file)
X = df[['mean_blue', 'mean_green', 'mean_red', 'std_blue', 'std_green', 'std_red']]
y = df['filename'].apply(lambda x: int(x.split('_')[1].split('.')[0]))  # Example: Extract group_id from filename

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred)
print(f"Model evaluation:\n{report}")

# Save model
joblib.dump(model, model_file)
print(f"Model trained and saved to {model_file}")
