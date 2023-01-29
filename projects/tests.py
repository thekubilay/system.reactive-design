from django.test import TestCase
from commons.crawlers import AsanaApiCrawler


crawler = AsanaApiCrawler()
crawler.get_projects()
crawler.get_tasks()
