import urllib.parse


class ExternalImages:
    def __init__(self, crawler):
        self.crawler = crawler
        self.images = []

    def get_results_header(self):
        return ["image"]

    def get_results(self):
        return [[image] for image in set(self.images)]

    def parse(self, html_soup, url=None):
        images = html_soup.find_all("img")
        parsed_base = urllib.parse.urlparse(self.crawler.base_url)

        for image in images:
            try:
                full_url = urllib.parse.urljoin(self.crawler.base_url, image["src"])
            except KeyError:
                continue

            parsed_url = urllib.parse.urlparse(full_url)
            if parsed_url.netloc != parsed_base.netloc:
                self.images.append(full_url)