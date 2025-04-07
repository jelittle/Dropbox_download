#handles auth and dropbox calls

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import os
from dotenv import load_dotenv

load_dotenv()
#create a .env file for these
APP_KEY = os.getenv("APP_KEY")
RERESH_TOKEN= os.getenv("REFRESH_TOKEN")
SCOPES=[]





def dbx_generator():
    """A generator function to always yield the same Dropbox client object with authentication."""
    def initialize():
        print("set the APP_KEY and REFRESH_TOKEN environment variables in a .env file")
        if input("enter y to get a refresh token")=='y':
            auth_flow=dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, use_pkce=True, token_access_type='offline')

            authorize_url = auth_flow.start()
            print("1. Go to: " + authorize_url)
            print("2. Click \"Allow\" (you might have to log in first).")
            print("3. Copy the authorization code.")
            auth_code = input("Enter the authorization code here: ").strip()
            try:
                oauth_result = auth_flow.finish(auth_code)
            except Exception as e:
                print('Error: %s' % (e,))
                exit(1)

            with dropbox.Dropbox(oauth2_refresh_token=oauth_result.refresh_token, app_key=APP_KEY) as dbx:
                
                dbx.users_get_current_account()
                print("connection successful, save the following token in a .env file and run again")
                print(oauth_result.refresh_token)
     
    load_dotenv()
    APP_KEY = os.getenv("APP_KEY")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
    if REFRESH_TOKEN is None:
        #refresh token not set, go through workflow to set one up
        initialize()
    dbx:None = None   # Store the Dropbox client object
   
    def generator():
        nonlocal dbx
        if dbx is None:  # Create the object only once
            dbx = dropbox.Dropbox(oauth2_refresh_token=REFRESH_TOKEN, app_key=APP_KEY)
            
        return dbx


    return generator()




 
 
  


