import os
import json

def create_new_folder(path):
    try:
        new_folder_path = os.path.join(path, "New Folder")
        os.makedirs(new_folder_path, exist_ok=True)
        return {'success': True, 'message': 'Folder created successfully', 'path': new_folder_path}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def get_storage_path():
    main_dir = os.path.dirname(os.path.abspath(__file__))
    storage_dir = os.path.join(main_dir, '..', 'storage')
    return storage_dir

def load_json_from_directory(json_path):
    """
    Load the specified JSON file at the given path.
    Args:
        json_filename (str): The path of the JSON file to be loaded.
    Returns:
        dict or list: The content of the JSON file.
    """
    # Check if the JSON file exists in the given directory
    if os.path.exists(json_path):
        # Load the JSON file and return its content
        with open(json_path, 'r') as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {json_path}: {e}")
                return None
    else:
        print(f"{json_path} not found")
        return None  

# The following acts like a call to get the data about all personas
def get_personas(storage_dir):
    # Construct the path to the 'persona' directory inside 'storage'
    persona_dir = os.path.join(storage_dir, 'persona')
    
    # Initialize a list to store all the personas
    personas = []
    
    # List all entries in the 'persona' directory
    for entry in os.listdir(persona_dir):
        # Create the full path to the entry
        entry_dir_path = os.path.join(persona_dir, entry)
        entry_path = os.path.join(entry_dir_path, 'profile')

        # Check if the entry is a directory
        if os.path.isdir(entry_path):
            # Look for 'persona.json' inside this first-level directory
            persona_path = os.path.join(entry_path, 'persona.json')
            persona_data = load_json_from_directory(persona_path)
            persona_data['path'] = entry_dir_path
            personas.append(persona_data)
    
    return personas


