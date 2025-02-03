

# Full Stack Development with NiceGUI, Flask, and SQLite

This document provides a step-by-step guide to setting up a very basic full-stack application using NiceGUI for the frontend, Flask for the backend, and SQLite for data storage.

## Prerequisites

* Python installed
* Basic understanding of Python and web development
* A virtual environment (optional but recommended)

## Step 1: Set Up the Project

Create a new directory for your project:

```sh
mkdir nicegui_flask_sqlite
cd nicegui_flask_sqlite
```

Create a virtual environment (optional but recommended):

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install the required dependencies:

```sh
pip install flask nicegui sqlite3
```

## Step 2: Set Up the Backend (Flask API)

Create a file `backend.py`:

```python
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS prompts (id INTEGER PRIMARY KEY, text TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.route("/process", methods=["POST"])
def process_prompt():
    data = request.json
    prompt = data.get("prompt", "")
    
    # Modify the prompt string (e.g., make it uppercase)
    processed_prompt = prompt.upper()
    
    # Store in SQLite
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prompts (text) VALUES (?)", (processed_prompt,))
    conn.commit()
    conn.close()
    
    return jsonify({"processed": processed_prompt})

if __name__ == "__main__":
    app.run(debug=True)
```

Run the backend server:

```sh
python backend.py
```

This will start the Flask API on `http://127.0.0.1:5000`.

## Step 3: Set Up the Frontend (NiceGUI)

Create a file `frontend.py`:

```python
from nicegui import ui
import requests

def send_prompt():
    response = requests.post("http://127.0.0.1:5000/process", json={"prompt": user_input.value})
    result_label.set_text(response.json().get("processed", "Error"))

ui.label("Enter a prompt:")
user_input = ui.input()
ui.button("Submit", on_click=send_prompt)
result_label = ui.label("Processed text will appear here.")

ui.run()
```

Run the frontend:

```sh
python frontend.py
```

This will start the NiceGUI frontend and open a web page.

## Step 4: Test the Application

1. Open the frontend in a browser.
2. Enter a text string and click "Submit".
3. The backend will process the string (convert it to uppercase) and return the result.
4. The processed string will be displayed on the frontend.

## Conclusion

This project demonstrates a minimal full-stack setup using:

* **NiceGUI** for frontend
* **Flask** for backend
* **SQLite** for data storage

This should provide a foundational understanding of full-stack web development with Python.
