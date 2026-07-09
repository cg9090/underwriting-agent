from ddgs import DDGS


class DuckDuckGoClient:

    def search(self, query: str, max_results=5):

        results = DDGS().text(
            query,
            max_results=max_results
        )

        return results