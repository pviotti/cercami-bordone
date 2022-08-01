import os
import scrapy
from scrapy.http import TextResponse

from ..items import TbfetcherItem


class PodcastSpider(scrapy.Spider):
    name = 'podcast'
    start_urls = ['https://www.ilpost.it/wp-login.php']


    def parse(self, response: TextResponse):
        return scrapy.FormRequest.from_response(
            response,
            formdata = {
                'log': os.environ["ILPOST_USER"],
                'pwd': os.environ["ILPOST_PASS"]
            },
            callback=self.after_login
        )


    def after_login(self, response: TextResponse):
        login_error = response.css("div#login_error").extract_first()
        if login_error:
            print(f"Found login error: {login_error}")
            return

        print("login succedeed!")
        return scrapy.Request(
                url="https://www.ilpost.it/podcasts/tienimi-bordone/",
                callback=self.parse_page)


    def parse_page(self, response: TextResponse):
        play_elements = [el for el in response.css("a.play") if "data-file" in el.attrib]
        for element in play_elements:
            item = TbfetcherItem()
            item["file_urls"] = [element.attrib["data-file"]]
            item["desc"] = element.attrib["data-desc"]
            item["title"] = element.attrib["data-title"]
            yield item

        next_page = response.css("a.next::attr(href)").extract_first()
        print(next_page)
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse_page
            )
