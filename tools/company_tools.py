from sources.companies_house import CompaniesHouseClient


client = CompaniesHouseClient()


def lookup_company(company_number: str):
    """
    Retrieve official company information from Companies House.
    """

    return client.get_company(company_number)