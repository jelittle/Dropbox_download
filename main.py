
import os


import files

"""todo: make command lineable"""
def main(path, root_path):
    os.makedirs("../" + root_path, exist_ok=True)
    # Set the root path for the download
    files.Folder.root_path = root_path
    # Create an instance of the Folder class
    folder = files.Folder.get(path)
    # Download the folder and its contents
    folder.download()



if __name__ == "__main__":
    path=
    root_path=
    main(path, root_path)

