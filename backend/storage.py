from google.cloud import storage  # Google Cloud Storage library
import os  # For file and path operations
import threading  # For asynchronous task execution
import requests  # For making HTTP requests
import ffmpeg  # Wrapper for FFmpeg, used for multimedia processing
from datetime import datetime  # For working with dates and times

# Configuration
BUCKET_NAME = "cps843"
API_ENDPOINT = "http://127.0.0.1:5000/motion_detected"

# Initialize the Google Cloud Storage client and bucket
STORAGE_CLIENT = storage.Client.from_service_account_json('credentials.json')
bucket = STORAGE_CLIENT.get_bucket(BUCKET_NAME)

def upload_to_bucket(blob_name, path_to_file):
    #Uploads a file to the bucket, makes it public, and returns its URL.
    #Deletes the local file after upload.
    blob = bucket.blob(blob_name)
    blob.content_type = 'video/mp4'
    blob.upload_from_filename(path_to_file)
    blob.make_public()
    os.remove(path_to_file)
    print(f"A new file by the name of {blob_name} was created in your bucket {BUCKET_NAME}")
    return blob.public_url

def handle_detection(path_to_file):
    #Processes a detected motion event by converting the file and uploading it.
    #Runs the operation in a separate thread.
    def action_thread(path_to_file):
        # Convert video resolution and upload the processed file
        output_path = path_to_file.split(".mp4")[0] + "-out.mp4"
        ffmpeg.input(path_to_file).output(output_path, vf='scale=-1:720').run()
        os.remove(path_to_file)
        
        try:
            url = upload_to_bucket(output_path, output_path)
            requests.post(API_ENDPOINT, json={"url": url})
        except Exception as e:
            print(f"Error in file handling: {e}")

    # Start the file processing in a new thread
    threading.Thread(target=action_thread, args=(path_to_file,)).start()

def list_videos_in_date_range(start_date, end_date, extension=".mp4"):
    #Lists videos in the bucket within a specified date range.
    #Filters by file extension and returns a list of matching file metadata.
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

    matching_files = []
    for blob in bucket.list_blobs():
        if blob.name.endswith(extension) and start_datetime <= blob.time_created.replace(tzinfo=None) <= end_datetime:
            matching_files.append({
                "url": blob.public_url,
                "date": blob.time_created.isoformat()
            })
            print(f"File {blob.name} matches date range.")  # Debugging

    return matching_files
