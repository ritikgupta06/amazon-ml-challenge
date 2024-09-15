import csv
import os
import requests
import datetime

# File paths
downloaded_images_log = 'data/downloaded_images.txt'
error_log = 'data/error_log.txt'
images_folder = 'images'

# Create images folder if it doesn't exist
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

# CSV file path
csv_file = 'data/your_file.csv'

# Download images
with open(csv_file, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        image_url = row['image_link']
        group_id = row['group_id']
        image_filename = f"image_{group_id}.jpg"
        image_path = os.path.join(images_folder, image_filename)

        if os.path.exists(image_path):
            print(f"{image_filename} already downloaded. Skipping...")
            continue

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
print("Download process complete.")
