from models.evidence import Evidence
from models.trade_press import TradePressArticle
from models.website import WebsiteContent

class EvidenceBuilder:

    def from_company_profile(self, company):

        evidence = []

        evidence.append(
            Evidence(
                claim=f"{company.company_name} is a registered company in the UK",
                category="company_information",
                source="Companies House",
                confidence=0.99
            )
        )

        if company.status:

            evidence.append(
                Evidence(
                    claim=f"Company status is {company.status}",
                    category="company_information",
                    source="Companies House",
                    confidence=0.99
                )
            )

        if company.sic_codes:

            evidence.append(
                Evidence(
                    claim=f"Company SIC codes are {company.sic_codes}",
                    category="business_model",
                    source="Companies House",
                    confidence=0.95
                )
            )

        return evidence

    def from_trade_press(
        self,
        article: TradePressArticle
    ):
        evidence = []

        evidence.append(
            Evidence(
                claim=article.title,
                category="quality_signal",
                source=article.source or "Trade Press",
                url=article.url,
                quote=article.content[:300],
                confidence=0.7
            )
        )
        
        return evidence
    
    def from_website(
    self,
    website
    ):

        evidence = []

        evidence.append(
            Evidence(
                claim="Company website provides information about its products and services",
                category="business_model",
                source="Company Website",
                url=website["url"],
                quote=website["content"][:500],
                confidence=0.7
            )
        )

        return evidence
    
    def from_competition(
    self,
    article
    ):

        evidence = []

        evidence.append(
            Evidence(
                claim=f"Competitive information identified from article: {article['title']}",
                category="competitive_landscape",
                source=article.get("source", "Trade Press"),
                url=article.get("url"),
                quote=article.get("content", "")[:500],
                confidence=0.6
            )
        )

        return evidence