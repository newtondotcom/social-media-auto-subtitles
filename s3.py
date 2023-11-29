import boto3

# Replace these with your AWS credentials and S3 bucket and file information
aws_access_key_id = 'your_access_key_id'
aws_secret_access_key = 'your_secret_access_key'
bucket_name = 'your_bucket_name'
file_key = 's3.txt'
local_file_path = 'local_path_to_save_downloaded_file.txt'

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

def download_file(file_key, local_file_path):
    try:
        s3.download_file(bucket_name, file_key, local_file_path)
        print(f"File downloaded successfully to {local_file_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")

def upload_file(file_key, local_file_path):
    try:
        s3.upload_file(local_file_path, bucket_name, file_key)
        print(f"File uploaded successfully to S3 key: {file_key}")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Uncomment the following lines to use the download and upload functions
# download_file(file_key, local_file_path)
# upload_file(file_key, local_file_path)
