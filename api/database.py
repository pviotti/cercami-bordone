import glob
import os
import re
import dataclasses
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
    date: str
    title: str
    url: str
    excerpts: list[str]

    def __repr__(self) -> str:
        res = f"{self.date} - {self.title}\n"
        for excerpt in self.excerpts:
            res += f"\t{excerpt}\n"
        return res

    def to_dict(self):
        return dataclasses.asdict(self)


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
        # dict respect insertion order in Python 3.7+
        self.db: dict[datetime, Transcription] = {}
        self._load_files()

    def _load_files(self, path: str = "./transcriptions", ext: str = "transcription"):
        """Load transcriptions into a dictionary."""

        files = sorted(glob.glob(f"{path}/*.{ext}"), reverse=True)

        for file_path in files:
            if "REPLAY" in file_path:
                continue

            with open(file_path, "r") as f:
                content = f.read()

            file_name = file_path.split(os.sep)[-1]
            date = datetime.strptime(file_name.split("_")[0], "%Y-%m-%d")
            title = file_name.split("_")[1].split(f".{ext}")[0]
            url = f"https://www.ilpost.it/episodes/{slugify(title)}/"
            transcr = Transcription(date=date, content=content, title=title, url=url)

            self.db[transcr.date] = transcr

    def reload_database(self):
        self.db.clear()
        self._load_files()

    def dump(self):
        print(self.db)

    def get_stats(self) -> dict:
        first_date = next(iter(self.db))
        return {
            "last_episode_date": self._date_to_str(first_date),
            "num_episodes": len(self.db),
        }

    def _date_to_str(self, date: datetime) -> str:
        return datetime.strftime(date, "%Y-%m-%d")

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
        return content[l_index:r_index]

    def _get_excerpts(self, content: str, term: str, length: int = 25) -> list[str]:
        start = 0
        f_index = 0
        excerpts = []
        while f_index != -1:
            f_index = content.find(term, start)
            if f_index != -1:
                excerpts.append(
                    self._build_excerpt_around_index(content, f_index, length)
                )
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
                gr = GrepResult(
                    self._date_to_str(transcr.date),
                    transcr.title,
                    transcr.url,
                    excerpts,
                )
                ret.append(gr)
            elif term in transcr.title.lower():
                gr = GrepResult(
                    self._date_to_str(transcr.date), transcr.title, transcr.url, []
                )
                ret.append(gr)
        return ret


if __name__ == "__main__":
    d = Database()
    # d.dump()
    term = input("Enter a term to grep for > ")
    if term:
        res = d.grep(term)
        for r in res:
            print(r)
