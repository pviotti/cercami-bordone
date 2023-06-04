import os
import calendar
import json
from datetime import datetime, date, timedelta
from typing import Optional, cast

from scrapy import Spider, FormRequest, Request
from scrapy.http import TextResponse

from ..items import TbfetcherItem

from dotenv import load_dotenv


load_dotenv(dotenv_path="../.env", verbose=True)


def get_last_day_of_month_before_previous(curr_day: date=date.today()) -> date:
    first_day_of_current_month = date(curr_day.year, curr_day.month, 1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = date(last_day_of_previous_month.year,
                                       last_day_of_previous_month.month, 1)
    return first_day_of_previous_month - timedelta(days=1)


class TbPodcastSpider(Spider):
    name = 'tbfetcher'

    def __init__(self, year: Optional[str] = None, month: Optional[str] = None, *args, **kwargs):
        super(TbPodcastSpider, self).__init__(*args, **kwargs)
        if year is None or month is None:
            self.limit_date = get_last_day_of_month_before_previous()
        else:
            year = int(year)
            month = int(month)
            self.limit_date = date(
                year, month, calendar.monthrange(year, month)[1])
        self.start_urls = ['https://www.ilpost.it/wp-login.php']

    def parse(self, _: TextResponse):
        username = os.environ["ILPOST_USER"]
        password = os.environ["ILPOST_PASS"]
        return [FormRequest(
            url="https://www.ilpost.it/wp-login.php",
            formdata={
                'log': username,
                'pwd': password,
                'rememberme': 'forever',
                'redirect_to': 'https://www.ilpost.it/podcasts/tienimi-bordone/',
                'testcookie': "1",
            },
            callback=self.after_login
        )]

    def after_login(self, response: TextResponse):
        login_error = response.css("div#login_error").extract_first()
        if login_error:
            print(f">>> Login error: {login_error}")
            return

        request = cast(FormRequest, response.request)
        request_cookies = cast(bytes, request.headers["Cookie"]).decode().split()
        loggedin_cookie = [c for c in request_cookies if "wordpress_logged_in" in c][0]
        loggedin_cookie_key = loggedin_cookie.split("=")[0]
        rdata = f"action=checkpodcast&cookie={loggedin_cookie_key}&post_id=0&podcast_id=227193"
        yield Request(url="https://www.ilpost.it/wp-admin/admin-ajax.php",
                      method="POST",
                      body=rdata,
                      headers={
                          "Accept": "application/json, text/javascript, */*; q=0.01",
                          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                          "Content-Length": len(rdata)
                      },
                      callback=self.parse_json)

    def parse_json(self, response: TextResponse):
        data = json.loads(response.text)["data"]
        for episode in data["postcastList"]:
            episode_date = datetime.strptime(episode['date'], "%Y-%m-%d %H:%M:%S").date()
            if episode_date > self.limit_date:
                item = TbfetcherItem()
                item["file_urls"] = [episode['podcast_raw_url']]
                item["date"] = episode_date
                item["title"] = episode["title"]
                yield item
