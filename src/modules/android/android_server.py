import asyncio
import json
import os
import time
import ctypes
from ctypes import wintypes
from fastapi import FastAPI, HTTPException, Request
from typing import Dict, Any
from src.android_phone import PhoneOps

# Load configuration data
def load_config(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)
config_path = os.path.join("src", "config", "config.json")
android_config = load_config(config_path)

# Initialize PhoneOps (without calling async_initialize here)
phone = PhoneOps(android_config)

# Define the FastAPI app
app = FastAPI()


# Path to torage folder
storage_path = r"C:\Users\gurpr\Documents\Coding\Projects\FastHTML_Test"

# Define a startup event to initialize PhoneOps asynchronously
@app.on_event("startup")
async def startup_event():
    await phone.async_initialize()

@app.post("/process-image")
async def process_image(request: Request):
    try:
        # Parse JSON body directly
        body = await request.json()
        image_path = body.get("image_path")
        data_object = body.get("data_object")

        # Log the received data to debug
        print("Received image_path:", image_path)
        print("Received data_object:", data_object)

        # Ensure image_path and data_object were provided
        if not image_path or data_object is None:
            raise HTTPException(status_code=400, detail="image_path and data_object are required")

        # Call perform_procedure with image_path and data_object
        result = await phone.perform_procedure(data_object)
        return {"status": "success", "result": result}
    except Exception as e:
        # Log the exact error for debugging
        print("Error in process_image:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process-payload")
async def process_payload(request: Request):
    try:
        # Parse JSON body directly
        body = await request.json()
        payload = body.get("payload", {})

        # Log the received data to debug
        print("Received payload:", payload)

        # Ensure payload and its main sections are provided
        if not payload or not payload.get("jobs") or not payload.get("info"):
            raise HTTPException(status_code=400, detail="Payload structure is incorrect or missing")

        # Iterate over jobs in the payload
        for i, job in enumerate(payload.get('jobs', [])):
            version_index = job.get("version-index", 0)
            
            # Get reference to the list of versions
            versions_list = job.get("item-data", {}).get("versions", [])
            if version_index >= len(versions_list):
                raise HTTPException(status_code=400, detail=f"Version index {version_index} out of range for job {i}")
            
            # Get reference to the specific version data
            version_data = versions_list[version_index]
            relative_path = version_data.get("url", "").replace("\\", "/")
            image_url = os.path.join(storage_path, relative_path)

            directory_path = os.path.dirname(image_url)
            print("Directory path:", directory_path)
            file_name_with_extension = os.path.basename(image_url)
            file_name = os.path.splitext(file_name_with_extension)[0]
            print("File name:", file_name)



            # Interact with the phone based on image_url (assuming phone object is defined)
            await set_file_creation_time_to_today(image_url)
            await phone.send_data_to_device(image_url)

            # Process edits for each job
            for edit in job.get("edits", []):
                try:
                    procedure = edit.get("procedure", {})
                    await phone.perform_procedure(procedure, image_url)
                    edit['status'] = "success"
                except Exception as e:
                    edit['status'] = "error"
                    edit['error'] = str(e)
                    print("Error in edit procedure:", e)

            # Pull data from device
            local_image_path = await phone.pull_data_from_device(directory_path, file_name)
            if local_image_path:
                # Update the version URL to the local image path in the original payload
                version_data['url'] = local_image_path.replace(storage_path, "").replace("\\", "/")
                print("UPDATED VERSION URL:", version_data['url'])

            # Delete the image sent and the edited saved image from the device
            await phone.delete_latest_two_images()

            # Update job status
            job['status'] = "completed" if all(edit.get("status") == "success" for edit in job.get("edits", [])) else "aborted"

        # Update job-index and final payload status
        payload["info"]["job-index"] += 1
        payload["info"]['status'] = "completed" if all(job.get("status") == "completed" for job in payload.get("jobs", [])) else "aborted"

        print("Final payload status:", payload['info']['status'])
        return {"status": "success", "result": payload}

    except Exception as e:
        print("Error in process_payload:", e)

        # Ensure payload is a dictionary to add error info
        if payload is None or not isinstance(payload, dict):
            payload = {}

        payload['status'] = "aborted"
        payload['error'] = str(e)
        
        print("Error in process_payload:", e)
        return {"status": "error", "result": payload}




async def set_file_creation_time_to_today(file_path):
    """
    Sets the creation, modification, and access times of the specified file to the current time (Windows only).
    Parameters:
    - file_path: Path to the file whose date you want to change.
    """
    # Get the current time in FILETIME format
    current_time = int((time.time() + 11644473600) * 10000000)
    filetime = ctypes.wintypes.FILETIME(current_time & 0xFFFFFFFF, current_time >> 32)

    # Open the file handle
    FILE_WRITE_ATTRIBUTES = 0x0100
    handle = ctypes.windll.kernel32.CreateFileW(
        file_path, FILE_WRITE_ATTRIBUTES, 0, None, 3, 0x02000000, None
    )

    if handle == ctypes.wintypes.HANDLE(-1).value:
        raise ctypes.WinError()

    # Set the creation, access, and modification times
    try:
        ctypes.windll.kernel32.SetFileTime(
            handle, ctypes.byref(filetime), ctypes.byref(filetime), ctypes.byref(filetime)
        )
    finally:
        ctypes.windll.kernel32.CloseHandle(handle)


# Run this with `uvicorn server_name:app --reload`
# cd src\modules\android
# uvicorn android_server:app