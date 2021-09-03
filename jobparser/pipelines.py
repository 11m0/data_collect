# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies3108

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['salary_min'], item['salary_max'], item['salary_val'] = self.process_salary_hh(item['salary'])
        if spider.name == 'sjru':
            item['salary_min'], item['salary_max'], item['salary_val'] = self.process_salary_sj(item['salary'])
        del item['salary']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        if salary:
            salary = salary.replace('\xa0', '')
            if salary.startswith('до'):
                salary_min = None
                salary_max = int(salary.partition(' ')[2].rpartition(' ')[0].replace(' ', ''))
                salary_val = salary.partition(' ')[2].rpartition(' ')[2]
            elif salary.startswith('от') and salary.find('до') == -1:
                salary_max = None
                salary_min = int(salary.partition(' ')[2].rpartition(' ')[0].replace(' ', ''))
                salary_val = salary.partition(' ')[2].rpartition(' ')[2]
            elif salary.startswith('з'):
                salary_min, salary_max, salary_val = None, None, None
            else:
                salary_min = int(salary.partition(' ')[2].partition(' ')[0])
                salary_max = int(salary.partition(' ')[2].partition(' ')[2].partition(' ')[2].partition(' ')[0])
                salary_val = salary.partition(' ')[2].rpartition(' ')[2]
        else:
            salary_min, salary_max, salary_val = None, None, None
        return salary_min, salary_max, salary_val

    def process_salary_sj(self, salary):
        if salary:
            salary = ''.join(salary)
            salary = salary.replace('\xa0', ' ')
            if salary.startswith('до'):
                salary_min = None
                salary_max = int(salary.partition(' ')[2].rpartition(' ')[0].replace(' ', ''))
                salary_val = salary.partition(' ')[2].rpartition(' ')[2]
            elif salary.startswith('от'):
                salary_min = int(salary.partition(' ')[2].rpartition(' ')[0].replace(' ', ''))
                salary_max = None
                salary_val = salary.partition(' ')[2].rpartition(' ')[2]
            elif salary.startswith('По'):
                salary_min, salary_max, salary_val = None, None, None
            elif (salary.startswith('до') and salary.startswith('от')) is False \
                    and salary.find('—') == -1:
                salary_min = salary_max = int(salary.rpartition(' ')[0].replace(' ', ''))
                salary_val = salary.rpartition(' ')[2]
            else:
                salary_min = int(salary.partition(' — ')[0].replace(' ', ''))
                salary_max = int(salary.partition(' — ')[2].rpartition(' ')[0].replace(' ', ''))
                salary_val = salary.partition(' — ')[2].rpartition(' ')[2]
            return salary_min, salary_max, salary_val
