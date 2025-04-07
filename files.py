from abc import ABC, abstractmethod
from Auth import dbx_generator
import dropbox
import os
import zipfile
import time
""""
todo:
list folders has file return limit of 2000, need list_folder/countinue if we want to handle all of them
try excpet design on api download errors could probably be better
"""
CHUNK_SIZE=30 #in mb



class DownloadItem(ABC):
    root_path="default"
    chunk_size=CHUNK_SIZE*1024*1024 #10MB
    def __init__(self, id,path,name):
        self.dbx=dbx_generator()
        self.id=id
        self.path=path
        self.name=name
        self.local_path = f"../{self.root_path}/{self.name}"  # save in parent directory+root path+own path
    @abstractmethod
    def download():
        pass
    def safe_remove(self, path):
        try:
            os.remove(path)
        except Exception as e:
            print(f"Error deleting file {path}: {e}")
    def save_in_system(self, res, format):
        local_file_path = self.local_path + format

        # Initial chunk size (100 MB)
        chunk_size = 10 * 1024 * 1024  # 10 MB
     

        total_size = 0
        file_size = int(res.headers.get('Content-Length', 0))  # File size in bytes
        start_time = time.time()

        try:
            if file_size > 3 * 1024**3:  # 3 GB
                print(f"Downloading {file_size / 1024**3:.2f} GB file")

            with open(local_file_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=chunk_size):
                    if chunk:  # Filter out keep-alive chunks
                        f.write(chunk)
                        total_size += len(chunk)

                        # Calculate progress and speed
                        elapsed_time = time.time() - start_time
                        progress = (total_size / file_size) * 100 if file_size > 0 else 0
                        speed_mbps = (total_size / 1_048_576) / elapsed_time if elapsed_time > 0 else 0

                        # Print progress
                        time_remaining = (file_size - total_size) / (speed_mbps * 1_048_576) if speed_mbps > 0 else float('inf')
                        print(
                            f"({progress:.2f}%) at {speed_mbps:.2f} MB/s, ETA: {time_remaining:.2f} seconds",
                            end="\r",
                        )


            print(f"\nDownload complete: {self.name}")
 

        except Exception as e:
            self.safe_remove(local_file_path)  # Remove the incomplete file
            print(f"Error saving file: {e}, removing incomplete file.")
                

    @classmethod
    def get(cls, path):
        """Create an instance of the specific subclass."""
        dbx = dbx_generator()
        response = dbx.files_get_metadata(path)
       
        # Dynamically create an instance of the calling subclass
        return cls(response.id, response.path_lower, response.name)
    

class Folder(DownloadItem):
    """a folder in dropbox"""

 
    def __init__(self, id,path,name):
        super().__init__(id,path,name)
        
        self.children=[]
  
    def unzip(self):
        #unzip the file
        #for now we just print the name of the file
       
        with zipfile.ZipFile(self.local_path+".zip", 'r') as zip_ref:
            extract_path = os.path.dirname(self.local_path)
            zip_ref.extractall(extract_path)
           
        # Delete the zip file after unzipping
        self.safe_remove(self.local_path+".zip")  # Remove the incomplete file
         
        
    def child_factory(self):
        """they yearn for the mines"""
        ret=[]
        #get all folder children
        children = self.dbx.files_list_folder(self.path)
        if children.has_more:
            #need to handle this
            pass
        #loop through all children, create appropriate instance
        for child in children.entries:
            child_name=f"{self.name}/{child.name}"
            if type(child)==dropbox.files.FolderMetadata:
            
                ret.append(Folder(child.id,child.path_lower,child_name))
            elif type(child)==dropbox.files.FileMetadata:
            
                if child.is_downloadable:
                    ret.append(downloadableFile(child.id,child.path_lower,child_name,child.size))
               
                else:
                    ret.append(exportableFile(child.id,child.path_lower,child_name,child.size))
                  
        return ret
         

    def download(self):
      
            
        try:
            #check if the folder already exists
            if os.path.exists(self.local_path):
      
                # print(f"{self.local_path} already exists. Skipping Full download.") 
                raise ValueError("File or folder already exists.")

            else:
                print(f"downloading {self.name} folder")
                start=time.time()
                
                meta,res=self.dbx.files_download_zip(self.path)
               
                self.save_in_system(res,".zip")
                self.unzip()
          

        except dropbox.exceptions.RateLimitError as e:
            print(f"Rate limit error encountered: {e}. Retrying after a delay.")
            time.sleep(10)
            self.download()
        #todo: relying on errors is probably bad design
        except (ValueError, dropbox.exceptions.ApiError) as e:
            if not isinstance(e, dropbox.files.DownloadZipError):
                if not isinstance(e, ValueError):
                    raise e

            
            #for now we just print error and pass downloading to children
            print(f"Error downloading {self.name}: {e}")
       
        
            os.makedirs(self.local_path, exist_ok=True)
            #find the children
            self.children=self.child_factory()
            for child in self.children:
                #create directory for children
                if not os.path.exists(child.local_path):
            
                    child.download()


        

class downloadableFile(DownloadItem):
    def __init__(self, id, path, name,size):
        super().__init__(id, path, name)
        self.size=size
    def download(self):
        
        try:
            if os.path.exists(self.local_path):
                #check if the file is the same size
                if os.path.getsize(self.local_path) == self.size:
                    print(f"{self.local_path} already exists. Skipping download.")
                    return 
                else:
                    print(f"File size mismatch for {self.local_path}. Downloading again.")
                    self.safe_remove(self.local_path)
                
                #slice the format out of the name
                format=self.name.split(".")[-1]

                #download files
                _,res=self.dbx.files_download(self.path)

                self.save_in_system(res,format)
      
        except dropbox.exceptions.RateLimitError as e:
            print(f"Rate limit error encountered: {e}. Retrying after a delay.")
            time.sleep(10)
            self.download()
class exportableFile(DownloadItem):
    def download(self):
        raise NotImplementedError("Export files not implemented.")
   





def main(path,root_path):
    os.makedirs("../"+root_path, exist_ok=True)
    # Set the root path for the download
    Folder.root_path = root_path
    # Create an instance of the Folder class
    folder = Folder.get(path)
    # Download the folder and its contents
    folder.download()







    
    