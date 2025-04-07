import files
import os
import argparse
import sys

# Replace 'path_to_venv' with the actual path to your virtual environment
venv_path = r"./venv/Scripts/activate"
if os.path.exists(venv_path):
    with open(venv_path) as f:
        exec(f.read(), {'__file__': venv_path})
else:
    print("Virtual environment activation script not found. Ensure the correct path is set.")
    sys.exit(1)

# def main(path, root_path):
#     os.makedirs("../" + root_path, exist_ok=True)
#     # Set the root path for the download
#     files.Folder.root_path = root_path
#     # Create an instance of the Folder class
#     folder = files.Folder.get(path)
#     # Download the folder and its contents
#     folder.download()



# def cli():
#     parser = argparse.ArgumentParser(description="Download files from a specified path.")
#     parser.add_argument("path", type=str, help="The path to the folder or file to download.")
#     parser.add_argument("root_path", type=str, help="The root path where the files will be downloaded.")
#     args = parser.parse_args()
#     main(args.path, args.root_path)
# if __name__ == "__main__":

#     # Call the main function with the parsed arguments
#     cli()