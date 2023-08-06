import json

def write_to_file(filename, content):
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Successfully wrote to {filename}.")
    except IOError:
        print(f"Error writing to {filename}.")

def read_dict_from_json(file_path):
    """
    Read a JSON file and return its contents as a Python dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a Python dictionary.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_dict_to_json(data, file_path):
    """
    Write a Python dictionary to a JSON file.

    Args:
        data (dict): The Python dictionary to be written.
        file_path (str): The path to the output JSON file.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file)