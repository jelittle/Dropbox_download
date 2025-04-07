
import os


import files

"""todo: make command lineable
async/parralel?
unzip progress bar
main only works with folders lol< get only works with folders lol
exportableFiles not complete
doesnt actually work with files larger than 20gb, well it does but I turned of exception handling on files.py line 175 ish to do it

"""
def main(path, root_path):
    os.makedirs("../" + root_path, exist_ok=True)
    # Set the root path for the download
    files.Folder.root_path = root_path
    # Create an instance of the Folder class
    folder = files.Folder.get(path)
    # Download the folder and its contents
    folder.download()



if __name__ == "__main__":
    path="/test/data/dng_files/profiles"
    root_path="test1"
    main(path, root_path)

