from sources.duckduckgo import DuckDuckGoClient
from sources.scraper import WebsiteScraper


class CompetitiveLandscapeClient:

    def __init__(self):
        self.search = DuckDuckGoClient()
        self.scraper = WebsiteScraper()


    def research(self, company_name: str):

        queries = [
            f"{company_name} competitors",
            f"{company_name} alternatives",
            f"{company_name} market analysis",
            f"{company_name} industry competition"
        ]

        articles = []

        # Find URLs
        for query in queries:

            results = self.search.search(
                query,
                max_results=3
            )

            articles.extend(results)


        # Remove duplicates
        seen = set()
        unique_articles = []

        for article in articles:

            url = article["href"]

            if url not in seen:
                seen.add(url)
                unique_articles.append(article)


        # Scrape first 5
        evidence_sources = []

        for article in unique_articles[:5]:

            page = self.scraper.scrape(
                article["href"]
            )

            if page["success"]:

                evidence_sources.append(
                    {
                        "title": article["title"],
                        "url": article["href"],
                        "content": page["content"]
                    }
                )


        return evidence_sources