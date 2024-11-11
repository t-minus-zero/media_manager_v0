import requests
import json
import os

# Define the absolute path to the image
image_path = r"C:\Users\gurpr\Documents\Coding\Projects\FastHTML_Test\storage\persona\Kiara\albums\adawong\ID-b450b1_I1_V1.jpg"
procedures_path = r"C:\Users\gurpr\Documents\Coding\Projects\FastHTML_Test\storage\procedures"

# Function to load all JSON files in the procedures_path directory
def load_procedures(procedures_dir):
    procedures_list = []
    for filename in os.listdir(procedures_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(procedures_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                procedures_list.append(data)
    return procedures_list

# Load procedures data from the specified directory
procedures = load_procedures(procedures_path)

# Choose a data object from the procedures (assuming it's a list of dictionaries)
data_object = procedures[0] if procedures else {}

# Define the URL of the FastAPI server
url = "http://127.0.0.1:8000/process-image"  # Adjust the port if necessary

# Prepare the payload
payload = {
    "image_path": image_path,
    "data_object": data_object
}

# Send the request to the FastAPI server
try:
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    print("Server response:", response.json())
except requests.exceptions.RequestException as e:
    print("Error communicating with the server:", e)
