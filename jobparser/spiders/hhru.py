import scrapy
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=python']

    def parse(self, response):
        urls = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.vacancy_parse)

    def vacancy_parse(self, response):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//p[@class='vacancy-salary']/span/text()").get()
        url = response.url
        item = JobparserItem(name=name, salary=salary, url=url)
        yield item
