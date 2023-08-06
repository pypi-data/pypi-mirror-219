import os


def get_absolute_path(file_path):
    return os.path.abspath(file_path)

def get_file_extension(file_path):
    return os.path.splitext(file_path)[1]

def get_file_size(file_path):
    return os.path.getsize(file_path)

def is_file_exists(file_path):
    return os.path.exists(file_path)

def mkdir(path):
    os.makedirs(path, exist_ok=True)

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except IOError:
        print(f"Error reading file '{file_path}'.")
        return None
    
def write_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
            print(f"Content written to file '{file_path}'.")
    except IOError:
        print(f"Error writing to file '{file_path}'.")