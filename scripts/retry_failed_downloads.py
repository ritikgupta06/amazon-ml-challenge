import os
import requests
import datetime

# File paths
error_log = 'data/error_log.txt'
downloaded_images_log = 'data/downloaded_images.txt'
images_folder = 'images'

# Function to extract image URL and filename from error log
def parse_error_log():
    failed_downloads = []
    with open(error_log, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if 'Failed to download' in line:
                parts = line.split('from ')
                if len(parts) == 2:
                    image_info = parts[1].split(':')[0].strip()
                    image_url, filename = image_info.split(' ')
                    failed_downloads.append((image_url, filename))
    return failed_downloads

# Retry failed downloads
failed_downloads = parse_error_log()
for image_url, filename in failed_downloads:
    image_path = os.path.join(images_folder, filename)
    if os.path.exists(image_path):
        print(f"{filename} already downloaded. Skipping...")
        continue

    try:
        print(f"Retrying download of {filename} from {image_url}...")
        response = requests.get(image_url)
        response.raise_for_status()

        with open(image_path, 'wb') as img_file:
            img_file.write(response.content)

        with open(downloaded_images_log, 'a') as log_file:
            log_file.write(f"{filename}\n")

        print(f"Downloaded and saved {filename}")

    except Exception as e:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_message = f"Failed to download {filename} from {image_url}: {str(e)} at {current_time}\n"
        with open(error_log, 'a') as error_file:
            error_file.write(error_message)

        print(f"Retry failed for {filename}. Error logged.")
