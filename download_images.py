import csv
import os
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor

downloaded_images_log = 'downloaded_images.txt'
error_log = 'error_log.txt'
images_folder = 'images'
max_workers = 5 

if not os.path.exists(images_folder):
    os.makedirs(images_folder)

csv_file = 'your_file.csv'

def download_image(row):
    image_url = row['image_link']
    group_id = row['group_id']
    image_filename = f"image_{group_id}.jpg"
    image_path = os.path.join(images_folder, image_filename)

    if os.path.exists(image_path):
        print(f"{image_filename} already downloaded. Skipping...")
        return

    try:
        print(f"Downloading {image_filename} from {image_url}...")
        response = requests.get(image_url)
        response.raise_for_status()

        with open(image_path, 'wb') as img_file:
            img_file.write(response.content)

        with open(downloaded_images_log, 'a') as log_file:
            log_file.write(f"{image_filename}\n")

        print(f"Downloaded and saved {image_filename}")

    except Exception as e:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_message = f"Failed to download {image_filename} from {image_url}: {str(e)} at {current_time}\n"
        with open(error_log, 'a') as error_file:
            error_file.write(error_message)

        print(f"Error downloading {image_filename}. Logged to error_log.txt.")

with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(download_image, csv_reader)

print("Download process complete.")
