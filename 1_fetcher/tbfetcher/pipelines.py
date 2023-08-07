# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from typing import Optional
from .items import TbfetcherItem


from scrapy.pipelines.files import FilesPipeline


class TbFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None, *,
                  item: Optional[TbfetcherItem]=None):
        return f"{item['date'].strftime('%Y-%m-%d')}_{item['title']}.mp3"
