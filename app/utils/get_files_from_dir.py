import os

def get_files_from_dir(directory):
    zip_file_list = []
    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            zip_file_list.append(filename)
    return zip_file_list