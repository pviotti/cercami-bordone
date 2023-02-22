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
        return f"{datetime.strftime(self.date, '%Y-%m-%d')} - {self.title}"

@dataclass
class GrepResult:
    date: datetime
    title: str
    url: str
    excerpts: list[str]

    def __repr__(self) -> str:
        res = f"{datetime.strftime(self.date, '%Y-%m-%d')} - {self.title}\n"
        for excerpt in self.excerpts:
            res += f"\t{excerpt}\n"
        return res

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

    def _build_excerpt_around_index(self, content: str, index: int, length: int) -> str:
        # left side
        l_index = index
        for _ in range(length // 2):
            l_index = content.rfind(" ", 0, l_index)
            if l_index == -1:
                break

        # right side
        r_index = index
        for _ in range(length // 2):
            r_index = content.find(" ", r_index + 1)
            if r_index == -1:
                break

        l_index = 0 if l_index == -1 else l_index
        r_index = len(content) if r_index == -1 else r_index
        return content[l_index : r_index]


    def _get_excerpts(self, content: str, term: str, length: int=20) -> list[str]:
        start = 0
        f_index = 0
        excerpts = []
        while f_index != -1:
            f_index = content.find(term, start)
            if f_index != -1:
                excerpts.append(self._build_excerpt_around_index(content, f_index, length))
                start = f_index + 1

        return excerpts


    def grep(self, term: str) -> list[GrepResult]:
        """Grep the database of transcriptions for a list of episodes
        that contain the given term.
        """
        ret = []
        for transcr in self.db.values():
            if term in transcr.content.lower():
                excerpts = self._get_excerpts(transcr.content.lower(), term)
                gr = GrepResult(transcr.date, transcr.title, transcr.url, excerpts)
                ret.append(gr)
        return ret


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
    # d.dump()
    # d.grep("telefono")
    res = d.grep("cucina")
    for r in res:
        print(r)
