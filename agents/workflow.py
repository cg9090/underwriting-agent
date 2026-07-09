from models.evidence import Evidence
from models.research import ResearchState

from sources.companies_house import CompaniesHouseClient
from sources.trade_press import TradePressClient
from sources.competitive_analysis import CompetitiveLandscapeClient

from sources.website_finder import WebsiteFinder
from sources.scraper import WebsiteScraper

from agents.evidence_builder import EvidenceBuilder
from agents.report_generator import ReportGenerator

from services.llm_extractor import LLMEvidenceExtractor

class UnderwritingAgent:

    def __init__(self):

        self.company_house = CompaniesHouseClient()

        self.website_finder = WebsiteFinder()

        self.scraper = WebsiteScraper()

        self.trade_press = TradePressClient()

        self.competition = CompetitiveLandscapeClient()

        extractor = LLMEvidenceExtractor()

        self.evidence_builder = EvidenceBuilder(extractor)

        self.report_generator = ReportGenerator()


    def investigate(
        self,
        company_input: str
    ):

        # Step 1: Resolve Company
        if company_input.isdigit():

            company = self.company_house.get_company(
                company_input
            )

        else:

            matches = self.company_house.search_company(company_input)

            if len(matches) == 0:

                return f"No companies found matching '{company_input}'."

            if len(matches) > 1:

                selected_company = self.choose_company(
                    matches
                )

            else:

                selected_company = matches[0]


            company = self.company_house.get_company(
                selected_company.company_number
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
        else:
            state.evidence.append(
                Evidence(
                    claim="Official company website could not be verified",
                    category="business_model",
                    source="Website Finder",
                    confidence=0.0,
                    limitations="No reliable official website found"
                )
            )

        # ------------------------
        # Trade Press
        # ------------------------

        articles = self.trade_press.search_articles(
            company.company_name
        )

        if len(articles) == 0:

            state.evidence.append(
                self.evidence_builder.create_evidence(
                    claim="No usable trade press sources were retrieved",
                    category="quality_signal",
                    source="Trade Press Search",
                    confidence=1.0
                )
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


        # report = self.report_generator.generate(
        #     state
        # )

        return state
    
    def choose_company(self, matches):

        print("\nMultiple companies found:\n")

        for index, company in enumerate(matches):

            print(
                f"{index}: "
                f"{company.company_name} | "
                f"{company.company_number} | "
                f"{company.company_status}"
            )


        choice = int(
            input("\nSelect company number: ")
        )


        return matches[choice]