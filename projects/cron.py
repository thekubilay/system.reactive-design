from commons.crawlers import AsanaApiCrawler

def crawl_asana():
  crawler = AsanaApiCrawler()
  crawler.get_projects()
  crawler.get_tasks()
