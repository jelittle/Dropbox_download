# Dropbox Large Download
Tool for downloading large files from dropbox. It is functional but definitely has some rough edges, check issues for more in-depth explanations
useful for downloading directly to servers rather than downloading to pc then through some rsync/scp..etc

## Features
- Automates downloading datasets from Dropbox.


## Installation
1. Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2. Install dependencies, ideally through venv but your choice:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Set up a Developper app through dropbox set the app_key a .env field
    ```
    APP_KEY=abced
    ```
2. Run the script once to get a refresh token and put it in a .env
    ```
    REFRESH_TOKEN=your_token_here
    ```
3. go to main.py and set root path and path. download root will be ../dropbox_download/root_path


## Project Structure


## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For questions or feedback, please contact me.
