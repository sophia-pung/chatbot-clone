import json

input_path = "../outputs/embeddings.json"
output_path = "../outputs/zilliz_formatted_embeddings.json"

# Load the raw JSON data
with open(input_path, "r") as f:
    raw_data = json.load(f)

# Extract and transform the data
formatted_data = {"rows": []}
for item in raw_data:
    vector = item["embedding"]
    text = item["text"].replace("\n", " ").strip()
    formatted_data["rows"].append({"vector": vector, "string": text})

# Save the transformed data to a new JSON file
with open(output_path, "w") as f:
    # Dump JSON with no space after separators like ':' and ','
    json.dump(formatted_data, f, indent=4, separators=(',', ':'))

print("Transformation complete!")