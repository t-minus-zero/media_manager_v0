import os

def create_new_folder(path):
    try:
        new_folder_path = os.path.join(path, "New Folder")
        os.makedirs(new_folder_path, exist_ok=True)
        return {'success': True, 'message': 'Folder created successfully', 'path': new_folder_path}
    except Exception as e:
        return {'success': False, 'message': str(e)}
