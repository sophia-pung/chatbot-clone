from flask import Flask, request, jsonify, render_template
import requests
import json
import sys

# Add the parent directory to the Python path to access config.py
sys.path.append("..")
from config import OPENAI_API_KEY, ZILLIZ_API_KEY, PUBLIC_ENDPOINT

app = Flask(__name__, template_folder='client')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create-embedding', methods=['POST'])
def create_embedding():
    text = request.json['query']
    
    # Generate the embedding using OpenAI API
    embedding = generate_embedding(text)
    
    # Find the closest matching texts using Zilliz vector search
    closest_texts = find_closest_matches(embedding)
    
    combined_text = combine_texts(closest_texts, threshold=0.71)
    print("Combined text:", combined_text, "END!!!!")
    
    return jsonify({"closest_texts": combined_text})

@app.route('/ask-question', methods=['POST'])
def ask_question():
    data = request.json
    question = data['question']
    document_text = data['documentText'][:28000]  # Ensure text is no longer than 30,000 characters

    answer = ask_gpt(question, document_text)
    
    return jsonify({"answer": answer})

def generate_embedding(text):
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "input": text,
        "model": "text-embedding-ada-002"
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['data'][0]['embedding']
    else:
        raise Exception(f"Failed to generate embedding: {response.status_code} {response.text}")

def find_closest_matches(embedding):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZILLIZ_API_KEY}"
    }
    
    payload = {
        "collectionName": "thunderstorm_vectors",
        "filter": "",
        "limit": 10,
        "outputFields": ["id", "text"],
        "vector": embedding
    }

    response = requests.post(f"{PUBLIC_ENDPOINT}/v1/vector/search", headers=headers, json=payload)
    print("Response JSON:", response.json())
    
    if response.status_code == 200:
        # Extract the 'data' list from the response
        data_list = response.json()['data']
        
        # Retrieve both text and distance for each result
        closest_texts_with_distances = [
            (item['text'], item['distance']) for item in data_list
        ]
        
        # If you only want the texts without the distances, uncomment the following line
        # closest_texts = [item['text'] for item in data_list]

        # Return the list of tuples with text and distance\
        print('CLOSEST TEXTS', closest_texts_with_distances, "distances", closest_texts_with_distances[0][1])
        return closest_texts_with_distances
        # Or just return 'closest_texts' if you don't need the distances
    else:
        raise Exception(f"Failed to find closest matches: {response.status_code} {response.text}")


def combine_texts(matches, threshold=0.71):
    print('MATCHESSSS', matches)
    # Assuming matches is a list of tuples in the form of [(text, distance), ...]
    # threshold = matches[0][1]
    # print('THRESHOLD', threshold)

    for text in matches:
        print("Type of text[1]:", type(text[1]), "Value of text[1]:", text[1])
        print("Type of threshold:", type(threshold), "Value of threshold:", threshold)
        print("TEXT 111",text[1])
        if text[1] > threshold:
            print("TEXT 333", text[1])
    filtered_texts = [text for text in matches if text[1] > threshold]
    test_text_distance = matches[0][1]
    print('TEST TEXT DISTANCE', test_text_distance)
    # texts = [text for text, distance in matches[0] if distance > threshold]
    print('FILTERED TEXTS', filtered_texts)
    print('FILTERED TEXTS', filtered_texts[0][0])
    filtered_texts = [text[0] for text in matches if text[1] > threshold]  # Extracting the text part of the tuple
    combined_text = " ".join(filtered_texts)
    return combined_text


def ask_gpt(question, document_text):
    print("Asking GPT...")

    # Estimated average token size is 4 characters per token, so 8192 tokens * 4 characters/token
    safe_character_limit = 8000 * 4
    if len(document_text) > safe_character_limit:
        document_text = document_text[:safe_character_limit]
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question},
            {"role": "assistant", "content": document_text}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("GPT response received successfully.", response.json())
        return response.json()['choices'][0]['message']['content']
    else:
        error_message = f"Failed to ask GPT: {response.status_code} {response.text}"
        print(error_message)
        raise Exception(error_message)

if __name__ == '__main__':
    app.run(debug=True)

