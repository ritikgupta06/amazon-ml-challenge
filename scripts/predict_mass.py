import pandas as pd
import cv2
import numpy as np
import joblib


images_folder = 'images'
model_file = 'models/model.pkl'
predictions_file = 'data/results/predictions.csv'


model = joblib.load(model_file)

def extract_features(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None

    mean_color = np.mean(img, axis=(0, 1))
    std_color = np.std(img, axis=(0, 1))

    return {
        'mean_blue': mean_color[0],
        'mean_green': mean_color[1],
        'mean_red': mean_color[2],
        'std_blue': std_color[0],
        'std_green': std_color[1],
        'std_red': std_color[2]
    }

predictions = []
for filename in os.listdir(images_folder):
    if filename.endswith('.jpg'):
        image_path = os.path.join(images_folder, filename)
        features = extract_features(image_path)
        if features:
            X = pd.DataFrame([features])
            predicted_group_id = model.predict(X)[0]
            predictions.append({
                'filename': filename,
                'predicted_group_id': predicted_group_id
            })

df = pd.DataFrame(predictions)
df.to_csv(predictions_file, index=False)
print(f"Predictions saved to {predictions_file}")
