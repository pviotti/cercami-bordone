#!/usr/bin/env python
# Script to transcribe mp3 files previously uploaded into a blob container.
# Modified version of this tutorial:
# https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch/python

import logging
import sys
import requests
import time
import swagger_client
import json
import time
import os
import glob
from dotenv import load_dotenv


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
        format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %I:%M:%S %p %Z")


load_dotenv(dotenv_path="../.env")


def getenv_or_exit(var: str) -> str:
    value = os.getenv(var)
    if not value:
        print(f"Error: value of {var} not specified")
        sys.exit(1)
    return value


NAME = "cercami-bordone"
DESCRIPTION = "A podcast transcription"
LOCALE = "it-IT"
SUBSCRIPTION_KEY = getenv_or_exit("AZURE_SUB_KEY")
SERVICE_REGION = getenv_or_exit("AZURE_REGION")
RECORDINGS_CONTAINER_URI = getenv_or_exit("AZURE_BLOB_CONTAINER_URI")
OUTPUT_PATH="../output/transcriptions"
ORIGINALS_PATH="../output/episodes-cut"


def transcribe_from_container(uri: str, properties: swagger_client.TranscriptionProperties):
    """Transcribe all files in the container located at `uri` using the settings specified in `properties`
    using the base model for the specified locale."""
    transcription_definition = swagger_client.Transcription(
        display_name=NAME,
        description=DESCRIPTION,
        locale=LOCALE,
        content_container_url=uri,
        properties=properties
    )

    return transcription_definition


def _paginate(api, paginated_object):
    """The autogenerated client does not support pagination. This function returns a generator over
    all items of the array that the paginated object `paginated_object` is part of."""

    yield from paginated_object.values
    typename = type(paginated_object).__name__
    auth_settings = ["api_key"]
    while paginated_object.next_link:
        link = paginated_object.next_link[len(api.api_client.configuration.host):]
        paginated_object, status, headers = api.api_client.call_api(link, "GET",
            response_type=typename, auth_settings=auth_settings)

        if status == 200:
            yield from paginated_object.values
        else:
            raise Exception(f"could not receive paginated data: status {status}")


def delete_all_transcriptions(api):
    """Delete all transcriptions associated with your speech resource."""
    logging.info("Deleting all existing completed transcriptions.")

    # get all transcriptions for the subscription
    transcriptions = list(_paginate(api, api.get_transcriptions()))

    # Delete all pre-existing completed transcriptions.
    # If transcriptions are still running or not started, they will not be deleted.
    for transcription in transcriptions:
        transcription_id = transcription._self.split('/')[-1]
        logging.debug(f"Deleting transcription with id {transcription_id}")
        try:
            api.delete_transcription(transcription_id)
        except swagger_client.rest.ApiException as exc:
            logging.error(f"Could not delete transcription {transcription_id}: {exc}")


def transcribe():
    start_time = time.time()
    logging.info("Starting transcription client...")

    # configure API key authorization: subscription_key
    configuration = swagger_client.Configuration()
    configuration.api_key["Ocp-Apim-Subscription-Key"] = SUBSCRIPTION_KEY
    configuration.host = f"https://{SERVICE_REGION}.api.cognitive.microsoft.com/speechtotext/v3.1"

    # create the client object and authenticate
    client = swagger_client.ApiClient(configuration)

    # create an instance of the transcription api class
    api = swagger_client.CustomSpeechTranscriptionsApi(api_client=client)

    # Specify transcription properties by passing a dict to the properties parameter. See
    # https://learn.microsoft.com/azure/cognitive-services/speech-service/batch-transcription-create?pivots=rest-api#request-configuration-options
    # for supported parameters.
    properties = swagger_client.TranscriptionProperties()
    # properties.word_level_timestamps_enabled = True
    # properties.display_form_word_level_timestamps_enabled = True
    # properties.punctuation_mode = "DictatedAndAutomatic"
    # properties.profanity_filter_mode = "Masked"
    # properties.destination_container_url = "<SAS Uri with at least write (w) permissions for an Azure Storage blob container that results should be written to>"
    # properties.time_to_live = "PT1H"

    # properties.language_identification = swagger_client.LanguageIdentificationProperties(["en-US", "ja-JP"])
    transcription_definition = transcribe_from_container(RECORDINGS_CONTAINER_URI, properties)

    created_transcription, status, headers = api.transcriptions_create_with_http_info(transcription=transcription_definition)

    # get the transcription Id from the location URI
    transcription_id = headers["location"].split("/")[-1]

    logging.info(f"Created new transcription with id '{transcription_id}' in region {SERVICE_REGION}")
    logging.info("Checking status.")
    completed = False

    try:
        while not completed:
            time.sleep(30)

            transcription = api.transcriptions_get(transcription_id)
            logging.info(f"Transcriptions status: {transcription.status}")

            if transcription.status in ("Failed", "Succeeded"):
                completed = True

            if transcription.status == "Succeeded":
                pag_files = api.transcriptions_list_files(transcription_id)
                for file_data in _paginate(api, pag_files):
                    if file_data.kind != "Transcription":
                        continue

                    audiofilename: str = file_data.name
                    results_url = file_data.links.content_url
                    logging.info(f"Getting content URL {results_url} for {audiofilename}...")
                    results = requests.get(results_url)
                    output_file = f"{OUTPUT_PATH}/{audiofilename.split('/')[1].strip('.mp3.json')}.transcription"
                    logging.info(f"Results for {audiofilename} written to {output_file}.")
                    # logging.info(f"Results for {audiofilename}:\n{results.content.decode('utf-8')}")
                    try:
                        json_data = json.loads(results.content.decode('utf-8'))
                        trascribed_txt = json_data["combinedRecognizedPhrases"][0]["display"]
                        with open(output_file, "w") as f:
                            f.write(trascribed_txt)
                    except Exception as e:
                        logging.warning(f"Error on {output_file} - {results_url} - {e}")

            elif transcription.status == "Failed":
                logging.info(f"Transcription failed: {transcription.properties.error.message}")

    finally:
        print(f"Transcription finished. It took {round(time.time() -start_time, 2)}s.")

        api.transcriptions_delete(transcription_id)
        logging.info(f"Transcription {transcription_id} deleted.")

        transcription_lst = api.transcriptions_list()
        print(f"Listing existing transcriptions: {transcription_lst}")


def _get_date_and_title(filepath: str) -> tuple[str, str]:
    filename = filepath.split(os.sep)[-1]
    filename_parts = filename.split("_")
    return filename_parts[0], filename_parts[1].split(".")[0]

def fix_transcriptions_titles(transcr_path: str = OUTPUT_PATH,
                              originals_path: str = ORIGINALS_PATH,
                              ext: str = "transcription"):
    """Azure Speech Services can't do proper UTF-8, so transcription file names
    have unrecognized characters. This function aims at fixing that."""

    originals = sorted(glob.glob(f"{originals_path}/*.mp3"))
    for original in originals:
        date, episode_title = _get_date_and_title(original)

        transcriptions = glob.glob(f"{transcr_path}/{date}*.{ext}")
        if len(transcriptions) != 1:
            print(f"****** WARNING: {len(transcriptions)} transcriptions found for {date} in {transcr_path}: will skip '{episode_title}'")
            continue

        _, transcription_title = _get_date_and_title(transcriptions[0])

        if transcription_title != episode_title:
            print(f"Found different title: {date} - {transcription_title} : {episode_title}")
            os.rename(transcriptions[0], f"{transcr_path}/{date}_{episode_title}.transcription")


if __name__ == "__main__":
    transcribe()
    fix_transcriptions_titles()