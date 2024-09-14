import os
import requests
import datetime

# Define the paths for logs and images
error_log = 'error_log.txt'
retry_log = 'retry_log.txt'
images_folder = 'images'

# Ensure the images folder exists
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

# Function to attempt download
def download_image(image_url, image_filename):
    try:
        print(f"Retrying download of {image_filename} from {image_url}...")
        response = requests.get(image_url)
        response.raise_for_status()

        # Save the image to the 'images' folder
        image_path = os.path.join(images_folder, image_filename)
        with open(image_path, 'wb') as img_file:
            img_file.write(response.content)

        # Log the successful download
        with open(retry_log, 'a') as log_file:
            log_file.write(f"{image_filename}\n")
        
        print(f"Successfully downloaded {image_filename}")

    except Exception as e:
        # Log the retry failure with timestamp
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_message = f"Retry failed for {image_filename} from {image_url}: {str(e)} at {current_time}\n"
        with open(error_log, 'a') as error_file:
            error_file.write(error_message)

        print(f"Retry failed for {image_filename}. Error logged.")

# Retry the failed downloads
if os.path.exists(error_log):
    with open(error_log, 'r') as error_file:
        error_lines = error_file.readlines()

    # Clear the error_log.txt to only record new errors from retries
    open(error_log, 'w').close()

    # Process each line in the error log
    for line in error_lines:
        # Skip empty lines
        if line.strip() == "":
            continue
        
        # Parse the error line
        try:
            # Look for the pattern: "Failed to download image_xxx.jpg: <error> at <time>"
            if "Failed to download" in line and "from" not in line:
                parts = line.split(":")
                image_filename = parts[0].split(" ")[3]
                # Here, you need to supply the image URL based on your logic, e.g., from a mapping or original CSV
                image_url = "your logic to retrieve URL here"  # Update this line with your actual logic

                # Retry downloading the image
                download_image(image_url, image_filename)
        
        except IndexError:
            print(f"Error parsing line: {line}")

else:
    print("No failed downloads found in error_log.txt.")
