# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
import locale
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline


class TbfetcherPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        datestr = item["desc"].split("-")[0].strip().replace(" ", "-")
        locale.setlocale(locale.LC_TIME, ('it', 'UTF-8'))
        date = datetime.strptime(datestr, '%d-%b-%Y')
        title = item["title"]
        return f"{date.strftime('%Y-%m-%d')}_{title}.mp3"
