#!/bin/bash
# Do the transcription steps in sequence.
# Pre-requisites:
# - venv activated with all requirements installed
# - .env file populated
set -ue

# 1. Crawl
echo "----------- Fetching -----------"
pushd 1_fetcher
scrapy crawl tbfetcher # -a year=2023 -a month=4
# Latest month that was transcribed
# Default: fetch all episodes more recent than the last day of the month before the previous
popd

# 2. Cut episodes
echo "----------- Cutting -----------"
pushd 2_cutter
./cut-episodes.sh
popd

# 3. Transcribe
echo "----------- Transcribing -----------"
pushd 3_transcriber
./uploader.py -u
./transcriber.py
popd

# 4. Add transcriptions to the web app
echo "----------- Uploading -----------"
echo "removed for public version"

# 5. Clean up
echo "----------- Clean up -----------"
rm -rf ./output/episodes-cut/*
rm -rf ./output/episodes-original/*
pushd 3_transcriber
./uploader.py -d
./uploader.py -l
popd