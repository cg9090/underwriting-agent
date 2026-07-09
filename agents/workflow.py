from models.research import ResearchState

from sources.companies_house import CompaniesHouseClient
from sources.trade_press import TradePressClient
from sources.competitive_analysis import CompetitiveLandscapeClient

from sources.website_finder import WebsiteFinder
from sources.scraper import WebsiteScraper

from agents.evidence_builder import EvidenceBuilder
from agents.report_generator import ReportGenerator


class UnderwritingAgent:

    def __init__(self):

        self.company_house = CompaniesHouseClient()

        self.website_finder = WebsiteFinder()

        self.scraper = WebsiteScraper()

        self.trade_press = TradePressClient()

        self.competition = CompetitiveLandscapeClient()

        self.evidence_builder = EvidenceBuilder()

        self.report_generator = ReportGenerator()


    def investigate(
        self,
        company_input: str
    ):

        # ------------------------
        # Resolve Company
        # ------------------------

        if company_input.isdigit():

            company = self.company_house.get_company(
                company_input
            )

        else:

            matches = self.company_house.search_company(
                company_input
            )

            if len(matches) == 0:

                raise ValueError(
                    "Company not found."
                )


            if len(matches) > 1:

                print("Multiple companies found:")

                for company in matches:

                    print(
                        company.company_name,
                        company.company_number
                    )

                raise ValueError(
                    "Company name is ambiguous. Please provide a company number."
                )


            company = self.company_house.get_company(
                matches[0].company_number
            )

        state = ResearchState(company_name=company.company_name)
        state.company = company

        # ------------------------
        # Companies House Evidence
        # ------------------------

        state.evidence.extend(

            self.evidence_builder.from_company_profile(
                company
            )

        )

        # ------------------------
        # Website
        # ------------------------

        website = self.website_finder.find(
            company.company_name
        )

        if website:

            website_content = self.scraper.scrape(
                website
            )

            state.evidence.extend(

                self.evidence_builder.from_website(
                    website_content
                )

            )

        # ------------------------
        # Trade Press
        # ------------------------

        articles = self.trade_press.search_articles(
            company.company_name
        )

        for article in articles:

            state.evidence.extend(

                self.evidence_builder.from_trade_press(
                    article
                )

            )

        # ------------------------
        # Competition
        # ------------------------

        competition_articles = self.competition.research(
            company.company_name
        )

        for article in competition_articles:

            state.evidence.extend(

                self.evidence_builder.from_competition(
                    article
                )

            )

        # ------------------------
        # Final Report
        # ------------------------
        print(state.evidence)

        for item in state.evidence:
            print(type(item))
        report = self.report_generator.generate(
            state
        )

        return report