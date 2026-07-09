from sources.duckduckgo import DuckDuckGoClient
from sources.scraper import WebsiteScraper
from models.trade_press import TradePressArticle

class TradePressClient:

    TRADE_SITES = [
        "techcrunch.com",
        "reuters.com",
        "ft.com",
        "sifted.eu",
        "uktech.news"
    ]

    def __init__(self):
        self.search = DuckDuckGoClient()
        self.scraper = WebsiteScraper()

    def search_articles(self, company_name: str):

        articles = []

        # Step 1: Find article URLs
        for site in self.TRADE_SITES:

            query = f"{company_name} site:{site}"

            results = self.search.search(query)

            articles.extend(results)


        # Step 2: Keep only first 5 articles
        articles = articles[:5]


        # Step 3: Scrape article content
        scraped_articles = []

        for article in articles:

            page = self.scraper.scrape(
                article["href"]
            )

            if page["success"]:

                scraped_articles.append(
                    TradePressArticle(
                        title=article["title"],
                        url=article["href"],
                        content=page["content"],
                        source=article.get("source")
                    )
                )

        return scraped_articles