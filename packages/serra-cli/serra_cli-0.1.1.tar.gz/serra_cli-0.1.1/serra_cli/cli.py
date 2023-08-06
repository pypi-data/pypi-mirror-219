# Entry point for serra command line tool
from os.path import exists
import click
import requests
from serra_cli.utils import write_to_file, read_dict_from_json, write_dict_to_json
import uuid
from os.path import exists
import re
import random
import string
from tqdm import tqdm
import time
import threading


LOCAL_BASE_URL = 'http://127.0.0.1:8000'
REMOTE_BASE_URL = "http://ec2-34-217-60-6.us-west-2.compute.amazonaws.com"
URL = f"{REMOTE_BASE_URL}/run"

def read_or_create_session_id():
    """
    TODO: Handle if file corrupted
    """

    path_to_session_dict = ".serra_config"

    if not exists(path_to_session_dict):
        # Create the session id file
        session_id = ''.join(random.choices(string.ascii_letters, k=10))
        d = {}
        d['session'] = session_id
        write_dict_to_json(d, path_to_session_dict)
        
    d = read_dict_from_json(path_to_session_dict)
    return d['session']
        
@click.group()
def main():
    pass

@main.command(name="start")
@click.argument("job_name")
def cli_start(job_name):
    """Create a yaml for job_name
    """
    file_path = f"{job_name}.yml"

    if exists(file_path):
        print("File already exists. Exiting.")
        exit()
    
    starter_config = f"name: {job_name}\njob_steps: []"
    write_to_file(file_path, starter_config)
    # create_job_yaml(job_name)


def simulate_progress(thread):
    total_items = 100  # Total number of items to process
    
    with tqdm(total=total_items, leave=False) as pbar:
        for _ in range(total_items):
            # Simulate processing an item
            time.sleep(0.1)  # Simulated processing time
            
            pbar.update(1)

            if not thread.is_alive():
                break
    
    # Clear the progress bar after completion
    pbar.close()


def send_post_request(file_path, url, session_id, response_holder):
    with open(file_path, 'rb') as file:
        # Send the POST request with the file
        response_holder['response'] = None
        try:
            response = requests.post(url, data={'session_id': session_id}, files={'file': file})
            # Store the response in the shared variable
            response_holder['response'] = response
        except: 
            pass

@main.command(name="run_local")
@click.argument("job_name")
def cli_run_job_from_job_dir(job_name):
    """Run a specific job
    """
    # Send config to aws
    # tell aws server to run code and wait for response
    # Set the URL of the Flask endpoint
    session_id = read_or_create_session_id()

    url = URL

    # Set the path to the local YAML file
    file_path = f"{job_name}.yml"

    # Read the contents of the YAML file
    response_holder = {}
    # Create a background thread and start it
    thread = threading.Thread(target=send_post_request, args=(file_path, url, session_id, response_holder))
    thread.start()
    simulate_progress(thread)
    thread.join()

    response = response_holder['response']

    if not response or response.status_code != 200:
        print("Error: Unable to connect to compute resources")
        return

    # Clean up logs for user and output
    print(response.text, end="")

if __name__ == '__main__':
  main()