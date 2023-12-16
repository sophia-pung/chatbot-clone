import json

# Specify the paths to your files using a relative path
input_path = "../outputs/test_embeddings.json"
output_path = "../outputs/formatted_embeddings.json"

# Load the current JSON file
with open(input_path, "r") as f:
    data = json.load(f)

# Extract and transform the data
transformed_data = []
for item in data:
    for embedding in item["data"]:
        vector = embedding["embedding"]
        transformed_data.append({"vector": vector})

# Save the transformed data to the new JSON file
with open(output_path, "w") as f:
    # Dump JSON with no space after separators like ':' and ','
    json.dump(transformed_data, f, indent=4, separators=(',', ':'))

print("Transformation complete!")
