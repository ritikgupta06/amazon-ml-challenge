import os
import cv2
import numpy as np
import pandas as pd

# File paths
images_folder = 'images'
features_file = 'data/features.csv'

# Function to extract features (example: basic image statistics)
def extract_features(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None

    # Example features
    mean_color = np.mean(img, axis=(0, 1))  # Mean color in BGR
    std_color = np.std(img, axis=(0, 1))    # Standard deviation of color

    return {
        'mean_blue': mean_color[0],
        'mean_green': mean_color[1],
        'mean_red': mean_color[2],
        'std_blue': std_color[0],
        'std_green': std_color[1],
        'std_red': std_color[2]
    }

# Extract features from all images
features_list = []
for filename in os.listdir(images_folder):
    if filename.endswith('.jpg'):
        image_path = os.path.join(images_folder, filename)
        features = extract_features(image_path)
        if features:
            features['filename'] = filename
            features_list.append(features)

# Save features to CSV
df = pd.DataFrame(features_list)
df.to_csv(features_file, index=False)
print(f"Features extracted and saved to {features_file}")
