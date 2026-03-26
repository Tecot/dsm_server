import os

def get_files_from_dir(directory):
    file_names = os.listdir(directory)
    return file_names