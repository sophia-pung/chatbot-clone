import requests
import json
import sys

# Add the parent directory to the Python path to access config.py
sys.path.append("..")
from config import PUBLIC_ENDPOINT, ZILLIZ_API_KEY

# Define the collection name
collection_name = "thunderstorm_vectors"

# Load the JSON data from file
with open('../outputs/zilliz_formatted_embeddings.json', 'r') as file:
    json_data = json.load(file)

# Set up the headers for the API request
headers = {
    "Authorization": f"Bearer {ZILLIZ_API_KEY}",
    "Content-Type": "application/json",
}

# Prepare the data to send with unique IDs
data_to_send = {
    "collectionName": collection_name,
    "data": [
        {
            "vector": row['vector'],
            "text": row['text']
        } for row in json_data['rows']
    ]
}

# Post the data to the API endpoint
response = requests.post(
    f"{PUBLIC_ENDPOINT}/v1/vector/insert",
    json=data_to_send,
    headers=headers,
)

# Print the response text to see if it was successful
print(response.text)