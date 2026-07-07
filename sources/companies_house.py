import os
import requests
from dotenv import load_dotenv

load_dotenv()


class CompaniesHouseClient:
    BASE_URL = "https://api.company-information.service.gov.uk"

    def __init__(self):
        self.api_key = os.getenv("COMPANIES_HOUSE_API_KEY")

        if not self.api_key:
            raise ValueError("COMPANIES_HOUSE_API_KEY not found.")
    
    def search_company(self, name: str):
        response = requests.get(
            f"{self.BASE_URL}/search/companies",
            params={"q": name},
            auth=(self.api_key, "")
        )

        response.raise_for_status()
        return response.json()

    def get_company(self, company_number: str):
        response = requests.get(
            f"{self.BASE_URL}/company/{company_number}",
            auth=(self.api_key, "")
        )

        response.raise_for_status()
        return response.json()