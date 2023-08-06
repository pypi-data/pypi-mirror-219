import yaml

from scholarly import scholarly
from scholarly import ProxyGenerator

from factool.env_config import factool_env_config

# env
scraper_api_key = factool_env_config.scraper_api_key

class google_scholar():
    def __init__(self):
        pg = ProxyGenerator()

        success = pg.ScraperAPI(scraper_api_key)
        scholarly.use_proxy(pg)

    def run(self, query):
        results = scholarly.search_pubs(query)
        paper_info = next(results)
        paper_info_subset = {key: paper_info['bib'][key] for key in ['title', 'author', 'pub_year']}
        return paper_info_subset

# Example Usage  
if __name__ == "__main__":
    tool = google_scholar()
    query = "Quantum approximate optimization algorithm: Performance, mechanism, and implementation on near-term devices"
    results = tool.run(query)
    print(results)