# Cercami Bordone

Speech to text experiment consisting in transcribing [podcast episodes][tb] and making them
searchable through a web application.

## Architecture

1. Podcast files retriever
2. Transcriber
3. Insert into database (SQLite?)
4. Expose transcriptions as a web app search engine


## APIs

### Azure Cognitive Services

https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/batch-transcription

https://westus.dev.cognitive.microsoft.com/docs/services/speech-to-text-api-v3-0/operations/CreateTranscription

Cost: 5h free per month (30 episodes)
```
0.952€ / h = 0.0158€ / min
0.015866667×10×650 = 103€ for all episodes
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