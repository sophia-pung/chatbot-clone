import requests
import json
import sys
# Add the parent directory to the Python path to access config.py
sys.path.append("..")
from config import OPENAI_API_KEY

def create_embeddings(text):
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "input": text,
        "model": "text-embedding-ada-002"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.json())  # Print the full response for debugging
    return response.json()

def chunk_text_by_lines(text, max_lines=450):
    lines = text.split('\n')
    chunks = [lines[i:i+max_lines] for i in range(0, len(lines), max_lines)]
    return ['\n'.join(chunk) for chunk in chunks]

if __name__ == "__main__":
    with open("thunderstorms.txt", "r", encoding="utf-8") as file:
        text = file.read()

    chunks = chunk_text_by_lines(text)
    all_embeddings = []

    for index, chunk in enumerate(chunks):
        print(f"Processing chunk {index + 1} with {len(chunk.split())} words:")
        print(chunk.split('\n')[0][:100] + "...")  # print the first 100 characters of the first line for context
        embeddings_response = create_embeddings(chunk)
        
        # Extract embedding value based on the provided structure
        if 'data' in embeddings_response and len(embeddings_response['data']) > 0:
            embedding_value = embeddings_response['data'][0].get('embedding', [])
        else:
            embedding_value = []

        embedding_data = {
            "index": index,
            "text": chunk,
            "embedding": embedding_value
        }
        
        all_embeddings.append(embedding_data)

        if "error" in embeddings_response:
            print(f"Error in chunk {index+1}: {embeddings_response['error']['message']}")

    with open("embeddings.json", "w", encoding="utf-8") as file:
        json.dump(all_embeddings, file, indent=4)
