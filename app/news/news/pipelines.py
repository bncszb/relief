# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import os


class NewsPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        os.makedirs("./cache/news", exist_ok=True)
        self.conn=sqlite3.connect("../cache/news/news.sqlite")
        self.curs=self.conn.cursor()

    def create_table(self):
        self.curs.execute("""drop table if exists news_table""")
        self.curs.execute("""create table news_table(
            title text,
            date text,
            link text,
            search_url text)
            """)
    def process_item(self, item, spider):

        self.store_db(item)
        return item

    def store_db(self, item):
        if len(item)>0:
            outp="(?"+", ?"*(len(item)-1)+")"
            self.curs.execute(f"""insert into news_table ({','.join([str(k) for k in item])}) values {outp}""", [str(v) for v in item.values()])
            self.conn.commit()