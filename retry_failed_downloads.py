import os
import requests
import datetime
error_log = 'error_log.txt'
retry_log = 'retry_log.txt'
images_folder = 'images'

if not os.path.exists(images_folder):
    os.makedirs(images_folder)

def download_image(image_url, image_filename):
    try:
        print(f"Retrying download of {image_filename} from {image_url}...")
        response = requests.get(image_url)
        response.raise_for_status()
        image_path = os.path.join(images_folder, image_filename)
        with open(image_path, 'wb') as img_file:
            img_file.write(response.content)
        with open(retry_log, 'a') as log_file:
            log_file.write(f"{image_filename}\n")
        print(f"Successfully downloaded {image_filename}")
    except Exception as e:

        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_message = f"Retry failed for {image_filename} from {image_url}: {str(e)} at {current_time}\n"
        with open(error_log, 'a') as error_file:
            error_file.write(error_message)

        print(f"Retry failed for {image_filename}. Error logged.")

if os.path.exists(error_log):
    with open(error_log, 'r') as error_file:
        error_lines = error_file.readlines()

    open(error_log, 'w').close()

    for line in error_lines:

        if line.strip() == "":
            continue
        
        try:

            if "Failed to download" in line and "from" not in line:
                parts = line.split(":")
                image_filename = parts[0].split(" ")[3]
      
                image_url = "your logic to retrieve URL here"  

        
                download_image(image_url, image_filename)
        
        except IndexError:
            print(f"Error parsing line: {line}")

else:
    print("No failed downloads found in error_log.txt.")
