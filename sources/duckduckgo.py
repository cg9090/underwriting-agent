import time
from ddgs import DDGS


class DuckDuckGoClient:

    def search(self, query: str, max_results=5):

        print(f"Searching: {query}")

        try:

            results = DDGS().text(
                query,
                max_results=max_results
            )

            return results

        except Exception as e:

            print(
                f"Search failed: {e}"
            )

            return []