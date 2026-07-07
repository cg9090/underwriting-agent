from sources.companies_house import CompaniesHouseClient

client = CompaniesHouseClient()

results = client.search_company("Monzo")

for company in results["items"]:
    print(company["title"])