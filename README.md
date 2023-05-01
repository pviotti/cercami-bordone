# Cercami Bordone

Speech-to-text experiment consisting in transcribing [podcast episodes][tb] and making them
searchable through a web application.

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

1. Crawl
    ```bash
    pushd 1_fetcher
    scrapy crawl tbfetcher
    popd
    ```
2. Cut episodes
    ```bash
    pushd 2_cutter
    ./cut-episodes.sh
    popd
    ```
3. Transcribe
    ```bash
    pushd 3_transciber
    ./uploader.py       # upload selected mp3 files interactively to Azure Storage
    ./transcriber.py    # create transcriptions (and fix their file names)
    popd
    ```
4. Add transcriptions to the web app
    ```bash
    make sync-transcr
    curl https://cb.vshed.xyz/reload-database
    ```

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

## Deploy web app

```bash
make build
make docker-push
make deploy
```

### Changes to configuration files in VPS

`docker-compose.yml`
```yml
  cercamibordone:
     image: pviotti/cercamibordone:latest
     container_name: cercamibordone
     restart: unless-stopped
     volumes:
      - ./data/cercamibordone:/app/transcriptions
```

`Caddyfile`
```text
cb.{$MY_DOMAIN} {
  reverse_proxy cercamibordone:5000

  log {
    output file /logs/cb.log
    level INFO
  }
}
```

## References

- [How to blur background in GIMP](https://thegimptutorials.com/how-to-blur-background/)
- [Whoosh, full text search library in Python](https://whoosh.readthedocs.io/en/latest/quickstart.html)
- [Azure Speech to Text API docs](https://westus.dev.cognitive.microsoft.com/docs/services/speech-to-text-api-v3-0/operations/CreateTranscription)
- [Azure Speech batch transcriptions docs](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/batch-transcription)
- [Azure Cognitive Services Python examples](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch/python)
- [Azure Storage Python examples](https://github.com/Azure/azure-storage-python/blob/master/samples/blob/block_blob_usage.py)
- [Azure Storage Python docs](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-python-get-started?tabs=azure-ad)
- [Azure Storage tips and tricks (post)](https://thats-it-code.com/azure/azure-blob-storage-operation-using-python/#python-azure-blob-storage-list-files)




[tb]: https://www.ilpost.it/podcasts/tienimi-bordone/