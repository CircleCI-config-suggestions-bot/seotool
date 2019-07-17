class DuplicateH1:
    def __init__(self, crawler):
        self.h1s = {}
        self.crawler = crawler

    def get_results_header(self):
        return ["h1", "urls"]

    def get_results(self):
        return [[h1, *urls] for (h1, urls) in self.h1s.items() if len(urls) > 1]

    def parse(self, html_soup, url=None):
        h1s = html_soup.find_all("h1")
        canonicals = html_soup.find_all("link", {"rel": "canonical"})
        if len(canonicals) > 0:
            try:
                url = canonicals[0]["href"]
            except KeyError:
                pass

        for h1Tag in h1s:
            h1 = h1Tag.getText()
            try:
                self.h1s[h1].append(url)
                self.h1s[h1] = list(set(self.h1s[h1]))
                self.crawler.printERR(f"H1 already seen on {', '.join(self.h1s[h1])}")
            except KeyError:
                self.h1s.update({h1: [url]})
