import logging
import subprocess
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def log_error(step_description, error):
    """
    Logs an error message with a detailed traceback.

    Args:
        step_description (str): Description of the step where the error occurred.
        error (Exception): The caught exception.
    """
    logger.error(f"Error at step: {step_description}")
    logger.error(f"Reason: {str(error)}")
    logger.error(traceback.format_exc())

def run_command(command):
    """
    Runs a shell command using subprocess and returns the result.

    Args:
        command (list): List of command arguments.

    Returns:
        str: Standard output from the command.

    Raises:
        Exception: If the command returns a non-zero exit code.
    """
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise Exception(f"Command failed: {' '.join(command)}, Error: {result.stderr}")
    except Exception as e:
        log_error(f"Running command: {' '.join(command)}", e)
        raise

def async_sleep(seconds):
    """
    Asynchronously sleep for the specified number of seconds.

    Args:
        seconds (int): Number of seconds to sleep.

    Returns:
        coroutine: Awaitable coroutine for sleeping.
    """
    import asyncio
    return asyncio.sleep(seconds)
