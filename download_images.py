import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import os
csv_file_path = 'dataset/train.csv'
save_directory = 'images/'
if not os.path.exists(save_directory):
    os.makedirs(save_directory)
df = pd.read_csv(csv_file_path)
print(f"Loaded {len(df)} rows from CSV.")
for index, row in df.iterrows():
    image_url = row['image_link'] 
    try:
        response = requests.get(image_url, timeout=10) 
        response.raise_for_status()  
        img = Image.open(BytesIO(response.content))
    
        file_name = f'image_{row["group_id"]}.jpg' 
        img.save(os.path.join(save_directory, file_name))
        
        print(f"Downloaded and saved {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image from {image_url}. Request error: {e}")
    except IOError as e:
        print(f"Failed to save image from {image_url}. IO error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

print("Image downloading completed.")
