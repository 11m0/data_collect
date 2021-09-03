import scrapy
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response):
        urls = response.xpath("//a[contains(@class, 'icMQ_ _6AfZ9')]/@href").getall()
        next_page = response.xpath("//a[contains(@class, 'f-test-link-Dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.vacancy_parse)

    def vacancy_parse(self, response):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//span[contains(@class, '_1OuF_ ZON4b')]/span[1]//text()").getall()
        url = response.url
        item = JobparserItem(name=name, salary=salary, url=url)
        yield item
