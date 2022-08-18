# Cercami Bordone

Speech to text experiment consisting in transcribing [podcast episodes][tb] and making them
searchable through a web application.

## Architecture

1. Retrieve podcast episodes
2. Cut initial and ending credits
3. Transcriber
4. Insert into database (SQLite?)
5. Expose transcriptions as a web app search engine


## APIs

### Azure Cognitive Services

https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/batch-transcription

https://westus.dev.cognitive.microsoft.com/docs/services/speech-to-text-api-v3-0/operations/CreateTranscription

Cost: 5h free per month (30 episodes)
```
0.952€ / h = 0.0158€ / min
0.015866667×10×650 = 103€ for all episodes
```

1. updload mp3 to storage account
2. create transcription
```bash
curl -X POST "https://uksouth.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions" \
-H "Content-Type: application/json" \
-H "Ocp-Apim-Subscription-Key: <subkey>" \
--data-ascii '{
  "contentUrls": [
    "https://tienimibordonespeech.blob.core.windows.net/tienimibordone/2022-07-28_Instagram perde colpi e cerca di insegnarmi l’amore.mp3"
  ],
  "properties": {
    "diarizationEnabled": false,
    "wordLevelTimestampsEnabled": false,
    "punctuationMode": "DictatedAndAutomatic",
    "profanityFilterMode": "Masked"
  },
  "locale": "it-IT",
  "displayName": "Transcription using default model for it-IT"
}'
```
Response:
```
{
  "self": "https://uksouth.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions/2fefde96-db52-44b6-8333-ced147b60356",
  "model": {
    "self": "https://uksouth.api.cognitive.microsoft.com/speechtotext/v3.0/models/base/bc7665d4-e3cb-41c2-82f9-c5de2d1a2f9c"
  },
  "links": {
    "files": "https://uksouth.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions/2fefde96-db52-44b6-8333-ced147b60356/files"
  },
  "properties": {
    "diarizationEnabled": false,
    "wordLevelTimestampsEnabled": false,
    "channels": [
      0,
      1
    ],
    "punctuationMode": "DictatedAndAutomatic",
    "profanityFilterMode": "Masked"
  },
  "lastActionDateTime": "2022-08-18T21:09:10Z",
  "status": "NotStarted",
  "createdDateTime": "2022-08-18T21:09:10Z",
  "locale": "it-IT",
  "displayName": "Transcription using default model for it-IT"
}
```
2. Get transcription status
```bash
curl https://uksouth.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions/2fefde96-db52-44b6-8333-ced147b60356 \
-H "Ocp-Apim-Subscription-Key: <subkey>" \
```
Response:
```
{
  "self": "https://uksouth.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions/2fefde96-db52-44b6-8333-ced147b60356",
  "model": {
    "self": "https://uksouth.api.cognitive.microsoft.com/speechtotext/v3.0/models/base/bc7665d4-e3cb-41c2-82f9-c5de2d1a2f9c"
  },
  "links": {
    "files": "https://uksouth.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions/2fefde96-db52-44b6-8333-ced147b60356/files"
  },
  "properties": {
    "diarizationEnabled": false,
    "wordLevelTimestampsEnabled": false,
    "channels": [
      0,
      1
    ],
    "punctuationMode": "DictatedAndAutomatic",
    "profanityFilterMode": "Masked",
    "duration": "PT9M33S"
  },
  "lastActionDateTime": "2022-08-18T21:12:47Z",
  "status": "Succeeded",
  "createdDateTime": "2022-08-18T21:09:10Z",
  "locale": "it-IT",
  "displayName": "Transcription using default model for it-IT"
}
```
3. Get transcription file URLs
```bash
curl https://uksouth.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions/2fefde96-db52-44b6-8333-ced147b60356/files
-H "Ocp-Apim-Subscription-Key: <subkey>"
```
Response:
```
{
  "values": [{
      "self": "https://uksouth.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions/2fefde96-db52-44b6-8333-ced147b60356/files/5641834c-109d-41aa-aff3-313ca6be2704",
      "name": "contenturl_0.json",
      "kind": "Transcription",
      "properties": {
        "size": 426385
      },
      "createdDateTime": "2022-08-18T21:12:47Z",
      "links": {
        "contentUrl": "https://spsvcproduks.blob.core.windows.net/bestor-948e9f4b-98f0-414a-b695-603be7bddabe/TranscriptionData/2fefde96-db52-44b6-8333-ced147b60356_0_0.json?sv=2021-06-08&st=2022-08-18T21%3A09%3A50Z&se=2022-08-19T09%3A14%3A50Z&sr=b&sp=rl&sig=LosgXORvovHQIoATmSNnzhbgGG%2BMtOWJXJgmymMJ%2FZA%3D"
      }
    },
    {
      "self": "https://uksouth.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions/2fefde96-db52-44b6-8333-ced147b60356/files/35163a8a-78f6-4fce-acf0-b74383cd14ef",
      "name": "report.json",
      "kind": "TranscriptionReport",
      "properties": {
        "size": 308
      },
      "createdDateTime": "2022-08-18T21:12:47Z",
      "links": {
        "contentUrl": "https://spsvcproduks.blob.core.windows.net/bestor-948e9f4b-98f0-414a-b695-603be7bddabe/TranscriptionData/2fefde96-db52-44b6-8333-ced147b60356_report.json?sv=2021-06-08&st=2022-08-18T21%3A09%3A50Z&se=2022-08-19T09%3A14%3A50Z&sr=b&sp=rl&sig=e0T3KsfYKfDki3VQd2CdwPDVEYaWA3WWydVPCiKKrFI%3D"
      }
    }
  ]
}
```
4. Get transcription
```bash
curl https://spsvcproduks.blob.core.windows.net/bestor-948e9f4b-98f0-414a-b695-603be7bddabe/TranscriptionData/2fefde96-db52-44b6-8333-ced147b60356_0_0.json?sv=2021-06-08&st=2022-08-18T21%3A09%3A50Z&se=2022-08-19T09%3A14%3A50Z&sr=b&sp=rl&sig=LosgXORvovHQIoATmSNnzhbgGG%2BMtOWJXJgmymMJ%2FZA%3D
| jq '.combinedRecognizedPhrases[0].display'
```


### Google Cloud Speech to Text API

https://cloud.google.com/speech-to-text/docs/async-recognize

Cost: https://cloud.google.com/speech-to-text/pricing

```
0.004$ / 15s
0.004 x 4 x 10 = 0.16$ per episode
0.16 x 650 = 104$ all episodes
```

### AWS Transcribe

using CLI: https://docs.aws.amazon.com/transcribe/latest/dg/getting-started-cli.html

tutorials: https://aws.amazon.com/transcribe/getting-started/?nc=sn&loc=4#Tutorials

Cost: ~150$ all episodes


## Retrieval and conversion of episodes


https://www.ilpost.it/podcasts/tienimi-bordone/feed/

Feed RSS does not link to mp3 file.
Might as well parse the HTML page with list of episodes daily.


## Useful commands

Convert to wav
```bash
ffmpeg -i tienimi-bordone-677-instagram-perde-colpi-e-cerca-di-insegnarmi-lamore.{mp3,wav}
```

Command line player
```bash
mpv tienimi-bordone-677-instagram-perde-colpi-e-cerca-di-insegnarmi-lamore.wav
```

Cut mp3 or wav file
```bash
ffmpeg -i tienimi-bordone-677-instagram-perde-colpi-e-cerca-di-insegnarmi-lamore.mp3 -vn -acodec copy -ss 00:00:16 -to 00:01:10 output.mp3
```




[tb]: https://www.ilpost.it/podcasts/tienimi-bordone/