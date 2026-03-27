import requests
import boto3
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# Load the environment variables from the .env file
load_dotenv()


# 1. CONFIGURATION (SECURELY LOADED)
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION')
BUCKET_NAME = os.getenv('BUCKET_NAME')
NASA_API_KEY = os.getenv('NASA_API_KEY')

# Check if key load properly
if not AWS_ACCESS_KEY:
    print("Error: AWS Credentials not found in .env file!")
    exit()


# 2. EXTRACT: Pull live data from NASA

print("Fetching Live Near-Earth Object data from NASA...")
date_today = datetime.now().strftime('%Y-%m-%d')
nasa_url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={date_today}&end_date={date_today}&api_key={NASA_API_KEY}"

response = requests.get(nasa_url)

if response.status_code == 200:
    raw_data = response.json()
    print(f"Success! Downloaded {raw_data['element_count']} asteroid records.")
else:
    print("Failed to fetch data from NASA API.")
    exit()

# 3. LOAD: Push the data into the S3 Data Lake

print("Connecting to AWS S3...")

# Initialize the S3 client using your secure service account

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# Create a unique filename based on the exact time of the run
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
s3_file_key = f"nasa_neo_data/raw_asteroids_{timestamp}.json"

print(f"Uploading data to S3 bucket: {BUCKET_NAME}...")

# Upload the JSON data directly to the Bronze layer
s3_client.put_object(
    Bucket=BUCKET_NAME,
    Key=s3_file_key,
    Body=json.dumps(raw_data)
)

print(f"Pipeline complete! File successfully loaded to S3 as '{s3_file_key}'.")