### Instructions for Setting Up the Project

1. **Set Up a Virtual Environment**
   - Navigate to `handbook_embeddings`.
   - Create a virtual environment: 
     ```bash
     python3 -m venv name-of-venv
     ```
   - Navigate to venv
   ```bash
    source name-of-venv/bin/activate 
    ```
   - ***Install Dependencies***

     Run (With pip installed):
     - `pip install Flask`
     - `pip install pdfminer`

2. **Configuration**
   - Create a `config.py` file inside of `handbook_embeddings`.
   - Add your OpenAI API key to this file.
   - Add Zilliz key to `config.py` file. 
         
         should look like: 
            -OPENAI_API_KEY = '';
            -PUBLIC_ENDPOINT = '';
            -ZILLIZ_API_KEY = '';

3. **Run the Script**
   - Activate your virtual environment (this step might vary depending on your OS).
      -Use chatGPT for specific command line prompts. e.g. "I'm on MacOS, how do I create a venv for a project I want to run"
   - Using current thunderstorms.txt file, (in your venv), run python3 app.py, and get the generated server for the client. 
   - Copy the server url from terminal and open in browswer. 
   - Enter your query, and the output will be logged in terminal. 
   - (If adding custom text file or pdf): Execute the script to generate embeddings for your txt file:
     ```bash
     python scripts/generate_embeddings.py
     ```
