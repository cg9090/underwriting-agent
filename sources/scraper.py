import requests
from bs4 import BeautifulSoup
from datetime import datetime


class WebsiteScraper:

    def scrape(self, url: str):

        try:
            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            response.raise_for_status()

        except requests.RequestException as e:
            return {
                "url": url,
                "success": False,
                "error": str(e),
                "content": None
            }


        soup = BeautifulSoup(
            response.text,
            "lxml"
        )


        # Remove irrelevant sections
        for element in soup(
            [
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "noscript"
            ]
        ):
            element.decompose()


        text = soup.get_text(
            separator=" ",
            strip=True
        )


        # Limit size so the LLM doesn't get flooded
        text = text[:10000]


        return {
            "url": url,
            "success": True,
            "content": text
        }