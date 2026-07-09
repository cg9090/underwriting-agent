from sources.duckduckgo import DuckDuckGoClient


class WebsiteFinder:

    def __init__(self):
        self.search = DuckDuckGoClient()
        self.IGNORED_DOMAINS = {
            "wikipedia.org",
            "linkedin.com",
            "facebook.com",
            "twitter.com",
            "instagram.com",
            "youtube.com"
        }

    def find(self, company_name: str):
        query = f"{company_name} official website"

        print(f"Searching website: {query}")
        results = self.search.search(
            f"{company_name} official website",
            max_results=5
        )

        if not results:
            return None

        # Prefer non-Wikipedia results
        for result in results:

            url = result["href"].lower()

            if any(domain in url for domain in self.IGNORED_DOMAINS):
                continue

            return result["href"]

        # Fall back to the first result if nothing better exists
        return results[0]["href"]