import os
import requests
from dotenv import load_dotenv

from models.company import CompanyProfile
from models.company_search import CompanySearchResult
from config import get_secret

load_dotenv()


class CompaniesHouseClient:
    BASE_URL = "https://api.company-information.service.gov.uk"

    def __init__(self):
        self.api_key = get_secret("COMPANIES_HOUSE_API_KEY")

        if not self.api_key:
            raise ValueError("COMPANIES_HOUSE_API_KEY not found.")
    
    def search_company(self, name: str):
        response = requests.get(
            f"{self.BASE_URL}/search/companies",
            params={"q": name},
            auth=(self.api_key, "")
        )

        response.raise_for_status()

        data = response.json()

        return [
        CompanySearchResult(
            company_name=item["title"],
            company_number=item["company_number"],
            company_status=item.get("company_status"),
            company_type=item.get("company_type")
        )
        for item in data.get("items", [])
    ]

    def get_company(self, company_number: str):
        response = requests.get(
            f"{self.BASE_URL}/company/{company_number}",
            auth=(self.api_key, "")
        )

        if response.status_code == 404:
            return None
        
        response.raise_for_status()

        data = response.json()

        return CompanyProfile(
            company_name=data["company_name"],
            company_number=data["company_number"],
            company_description=data.get("description"),
            status=data.get("company_status"),
            company_links=data.get("links", {}),
            incorporation_date=data.get("date_of_creation"),
            sic_codes=data.get("sic_codes", []),
            registered_address=str(
                data.get("registered_office_address", {})
            )
        )