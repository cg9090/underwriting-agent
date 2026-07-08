# from sources.companies_house import CompaniesHouseClient

# client = CompaniesHouseClient()

# company = client.get_company("09446231")

# print(company)
# print(company.company_name)
# print(company.sic_codes)

# from sources.duckduckgo import DuckDuckGoClient


# client = DuckDuckGoClient()

# results = client.search(
#     "LinkedIn official website"
# )

# for result in results:
#     print(result["title"])
#     print(result["href"])
#     print("---")

from sources.scraper import WebsiteScraper


scraper = WebsiteScraper()

text = scraper.scrape(
    "https://monzo.com"
)

print(text[:1000])