import os
import glob
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv


load_dotenv()
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "tienimibordone"

print_lock = Lock()

def p(string: str):
    with print_lock:
        print(string)

def upload_file(file_name: str):
    blob_name = file_name.split("/")[-1]
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open(file_name, "rb") as data:
        blob_client.upload_blob(data)
    p(f"Uploaded: {file_name}")


def main():
    while True:
        res = input("Select [l,d,u,q] > ")

        if res == 'q':
            break

        elif res == 'l':
            try:
                list_response = blob_service_client.get_container_client(container_name).list_blobs()
                count = 0
                for r in list_response:
                    print(r.name)
                    count += 1
                print(f"Total: {count} blobs")
            except Exception as e:
                print("Failed to get the blob list in the container. Error:" + str(e))

        elif res == 'u':
            prefix = input("Input the prefix of files to upload: ")
            files = glob.glob(f"./episodes-cut/{prefix}*.mp3")

            with ThreadPoolExecutor(10) as executor:
                executor.map(upload_file, files)

            print(f"Finished upload of {len(files)}.")

        elif res == 'd':
            res = input(f"Delete all blobs in {container_name}? [y,n]: ")
            if res == 'y':
                container_client = blob_service_client.get_container_client(container_name)
                blob_list = container_client.list_blobs()
                container_client.delete_blobs(*blob_list, delete_snapshots="include")
                print(f"Deleted all blobs from {container_name}.")


if __name__ == '__main__':
    main()