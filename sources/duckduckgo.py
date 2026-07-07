from ddgs import DDGS


class DuckDuckGoClient:

    def search(self, query: str):

        results = DDGS().text(
            query,
            max_results=5
        )

        return results