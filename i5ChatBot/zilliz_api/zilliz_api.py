import requests
import json
from config import PUIBLIC_ENDPOINT, ZILLIZ_API_KEY

BASE_URL = f"{PUIBLIC_ENDPOINT}/v1/vector"

HEADERS = {
    "content-type": "application/json",
    "Authorization": f"Bearer {ZILLIZ_API_KEY}"
}

def get_collections():
    """Fetch all vector collections from the Zilliz API."""
    response = requests.get(f"{BASE_URL}/collections", headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def insert_data():
    """Inserts data into the Zilliz API."""
    # Load data from the JSON file
    with open("/Users/sophiapung/Documents/Projects/handbook_embeddings/outputs/zilliz_formatted_embeddings.json", "r") as f:
        data = json.load(f)

    payload = {
        "collectionName": "thunderstorm_vectors",
        "data": data
    }

    response = requests.post(f"{BASE_URL}/insert", headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

if __name__ == "__main__":
    # Commented out the get_collections function for now
    # collections = get_collections()
    # print(collections)

    # Insert data
    response = insert_data()
    print(response)
