import os
import glob

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "tienimibordone"


def main():
    while True:
        res = input("Select [l,d,u,q]: ")

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

            # TODO: parallelize
            for file in files:
                blob_name = file.split("/")[-1]
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
                with open(file, "rb") as data:
                    blob_client.upload_blob(data)
                print(f"Uploaded: {file}")

        elif res == 'd':
            res = input(f"Delete all blobs in {container_name}? [y,n]: ")
            if res == 'y':
                container_client = blob_service_client.get_container_client(container_name)
                blob_list = container_client.list_blobs()
                container_client.delete_blobs(*blob_list, delete_snapshots="include")
                print(f"Deleted all blobs from {container_name}.")


if __name__ == '__main__':
    main()