# from flask import Flask, send_from_directory
# from flask_restful import Api, Resource, reqparse
# from flask_cors import CORS #comment this on deployment
# from api.HelloApiHandler import HelloApiHandler

# app = Flask(__name__, static_url_path='', static_folder='frontend/build')
# CORS(app) #comment this on deployment
# api = Api(app)

# @app.route("/", defaults={'path':''})
# def serve(path):
#     return send_from_directory(app.static_folder,'index.html')

# api.add_resource(HelloApiHandler, '/flask/hello')

import glob
import os
import re
from dataclasses import dataclass
from datetime import datetime
import unicodedata


@dataclass(order=True)
class Transcription:
    date: datetime
    content: str
    title: str
    url: str

    def __repr__(self) -> str:
        return datetime.strftime(self.date, "%Y-%m-%d") + " - " + self.title


def slugify(value, allow_unicode: bool = False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    From Django source code: https://github.com/django/django/blob/main/django/utils/text.py#L420
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


class Database:
    def __init__(self):
        self.db: dict[datetime, Transcription] = {}
        self._load_files()

    def _load_files(self, path: str = "transcriptions", ext: str = "transcription"):
        """Load transcriptions into a dictionary."""

        files = glob.glob(f".{os.sep}{path}{os.sep}*.{ext}")

        for file_path in files:
            with open(file_path, "r") as f:
                content = f.read()

            file_name = file_path.split(os.sep)[-1]
            date = datetime.strptime(file_name.split("_")[0], "%Y-%m-%d")
            title = file_name.split("_")[1].split(f".{ext}")[0]
            url = f"https://www.ilpost.it/episodes/{slugify(title)}/"
            transcr = Transcription(
                date=date,
                content=content,
                title=title,
                url=url
            )

            self.db[transcr.date] = transcr

    def dump(self):
        print(self.db)

    def grep(self, term: str) -> list[Transcription]:
        """Grep the database of transcriptions for a list of episodes
        that contain the given term."""
        for key, val in self.db.items():
            if term in val.content.lower():
                print(self.db[key])


def _get_date_title(filepath: str) -> tuple[str, str]:
    filename = filepath.split(os.sep)[-1]
    filename_parts = filename.split("_")
    date, title = filename_parts[0], filename_parts[1].split(".")[0]
    return date, title


def fix_transcriptions_titles(path: str = "transcriptions", ext: str = "transcription"):
    """Azure Speech Services can't do proper UTF-8, so transcription file names
    have unrecognized characters. This function aims at fixing that."""

    transcriptions = glob.glob(f".{os.sep}{path}{os.sep}*.{ext}")
    for transcr in transcriptions:
        date, title = _get_date_title(transcr)

        episodes = glob.glob(f"./episodes-cut/{date}*.mp3")
        _, episode_title = _get_date_title(episodes[0])

        if title != episode_title:
            print(f"Found different title: {date} - {title} : {episode_title}")
            os.rename(transcr, f"./transcriptions/{date}_{episode_title}.transcription")


if __name__ == "__main__":
    # fix_transcriptions_titles()
    d = Database()
    d.dump()
    d.grep("telefono")
