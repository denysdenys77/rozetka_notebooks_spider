from scrapy_selenium import SeleniumRequest
import scrapy
import sqlalchemy as db
from dotenv import load_dotenv
import os

load_dotenv()


class NotebookSpider(scrapy.Spider):
    name = 'note'
    start_urls = ['https://rozetka.com.ua/notebooks/c80004/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = db.create_engine(f'mysql+pymysql://'
                                       f'{os.getenv("DB_USERNAME")}:'
                                       f'{os.getenv("DB_PASSWORD")}@localhost/'
                                       f'{os.getenv("DB_NAME")}')
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, wait_time=3, callback=self.parse)

    def parse(self, response):
        rozetka_notebooks = db.Table('rozetka_notebooks', self.metadata, autoload=True, autoload_with=self.engine)
        for item in response.css('div.goods-tile__inner'):
            name = item.css('span.goods-tile__title::text').get()
            price = item.css('span.goods-tile__price-value::text').get()
            str_name = name.encode('ascii', errors='ignore').decode('utf-8')

            # writing data to MySQL database
            query = db.insert(rozetka_notebooks).values(name=str_name,
                                                        price=price)
            self.connection.execute(query)

            # returning data to terminal or json
            # yield {
                # 'name': str_name,
                # 'price': price,
            # }

        next_page = response.xpath('//rz-paginator/div/a[2]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield SeleniumRequest(url=next_page, wait_time=3, callback=self.parse)

