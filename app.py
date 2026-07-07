from sources.companies_house import CompaniesHouseClient

client = CompaniesHouseClient()

company = client.get_company("09446231")

print(company)
print(company.company_name)
print(company.sic_codes)