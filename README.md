# Cercami Bordone

This is a speech-to-text experiment consisting in transcribing episodes of [a podcast][tb]
and making the transcriptions searchable through a web application.

Steps involved:
1. Retrieve podcast episodes
2. Cut initial and ending credits
3. Upload cut episodes to Azure Storage
4. Transcribe episodes in Azure Storage using Azure Speech Services
4. Expose transcriptions as a search engine web application

## Setup

1. Install required Python packages
    ```bash
    python -m venv venv
    source venv/bin/activate
    python -m pip install -r requirements.txt
    ```
2. Setup secrets in `.env` file
    ```
    AZURE_SUB_KEY: Azure Speech Services subscription key
    AZURE_REGION: Azure Speech Services region
    AZURE_STORAGE_CONNECTION_STRING: Azure Storage Account connection key (Storage account > Access keys)
    AZURE_BLOB_CONTAINER_URI: Azure Container URL (Container > Shared access token - Read and List rights)
    ILPOST_USER: Il Post username
    ILPOST_PASS: Il Post password
    ```
3. Setup output folders
    ```bash
    mkdir -p output/episodes-original output/episodes/cut output/transcriptions
    ln -s $(pwd)/output/transcriptions api/transcriptions
    ```

## Add new transcriptions

Run `./create_transcriptions.sh`.

## Develop web app

Start frontend development server:
```bash
cd frontend
npm start
# to build the React application in ./api/static
npm run build
```
Start API server:
```bash
cd api
flask --debug --app server run
```

## References

- [Azure Speech to Text API docs](https://westus.dev.cognitive.microsoft.com/docs/services/speech-to-text-api-v3-0/operations/CreateTranscription)
- [Azure Speech batch transcriptions docs](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/batch-transcription)
- [Azure Cognitive Services Python examples](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch/python)
- [Azure Storage Python examples](https://github.com/Azure/azure-storage-python/blob/master/samples/blob/block_blob_usage.py)
- [Azure Storage Python docs](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-python-get-started?tabs=azure-ad)
- [Azure Storage tips and tricks (post)](https://thats-it-code.com/azure/azure-blob-storage-operation-using-python/#python-azure-blob-storage-list-files)
- [Whoosh, full text search library in Python](https://whoosh.readthedocs.io/en/latest/quickstart.html)
- [How to blur background in GIMP](https://thegimptutorials.com/how-to-blur-background/)



[tb]: https://www.ilpost.it/podcasts/tienimi-bordone/