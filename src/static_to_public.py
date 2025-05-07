import os
import shutil

def clean_destination(path):
    #Destination exists rm it
    if os.path.exists(path): 
        print(f'Removed the directory: {path}')
        shutil.rmtree(path)
    
    #Making the Directory destination if it doesn't exist
    os.makedirs(path)
    print(f"Made directory: {path}")

def copy_dirr(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)
    
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isdir(source_path):
            copy_dirr(source_path, destination_path)
        else:
            shutil.copy2(source_path, destination_path)
            print(f"Copied {source_path} -> {destination_path}")

def static_to_public():
    source = "./static"
    destination = "./docs"
    print(f'Cleaning Destination: {destination}')
    clean_destination(destination)
    print(f'Copying Files')
    copy_dirr(source, destination)
    print("Complete")
    