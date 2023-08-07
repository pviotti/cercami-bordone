#!/usr/bin/env python3
# Module to upload to and delete mp3s from Azure Storage.

import os
import glob
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from argparse import ArgumentParser

from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv


load_dotenv(dotenv_path="../.env")
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

FILES_PATH="../output/episodes-cut"

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


def upload_files(prefix: str=""):
    files = sorted(glob.glob(f"{FILES_PATH}/{prefix}*.mp3"))

    # XXX threadpoolexecutor seems slow
    # with ThreadPoolExecutor(10) as executor:
    #     executor.map(upload_file, files)
    for file in files:
        if "REPLAY" in file:
            continue
        upload_file(file)

    print(f"Finished upload of {len(files)}.")


def delete_files():
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blobs()
    container_client.delete_blobs(*blob_list, delete_snapshots="include")
    print(f"Deleted all blobs from {container_name}.")


def list_files():
    try:
        list_response = blob_service_client.get_container_client(container_name).list_blobs()
        count = 0
        for r in list_response:
            print(r.name)
            count += 1
        print(f"Total: {count} blobs")
    except Exception as e:
        print("Failed to get the blob list in the container. Error:" + str(e))


def interactive():
    while True:
        res = input("Select [l,d,u,q] > ")

        if res == 'q':
            break

        elif res == 'l':
            list_files()

        elif res == 'u':
            prefix = input("Input the prefix of files to upload: ")
            upload_files(prefix)

        elif res == 'd':
            res = input(f"Delete all blobs in {container_name}? [y,n]: ")
            if res == 'y':
                delete_files()


if __name__ == '__main__':
    parser = ArgumentParser('Episode uploader',
                            'Uploads files to or removes them from Azure storage.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--upload', '-u', action='store_true')
    group.add_argument('--delete', '-d', action='store_true')
    group.add_argument('--list', '-l', action='store_true')
    args = parser.parse_args()

    if args.upload:
        upload_files()
    elif args.delete:
        delete_files()
    elif args.list:
        list_files()
    else:
        interactive()