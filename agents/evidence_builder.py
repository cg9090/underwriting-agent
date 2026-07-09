from models.evidence import Evidence
from models.article import Article

class EvidenceBuilder:

    def __init__(self, extractor):
        self.extractor = extractor

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

        if company.company_description:

            evidence.append(
                Evidence(
                    claim=f"Company description: {company.company_description}",
                    category="business_model",
                    source="Companies House",
                    confidence=0.9
                )
            )

        return evidence

    def from_trade_press(
        self,
        article: Article
    ):
        result = self.extractor.extract(
            text=article.content,
            category="quality_signal"
        )

        if result.error:
            return []
        
        evidence = []

        for claim in result.claims:

            evidence.append(
                Evidence(
                    claim=claim["claim"],
                    category="quality_signal",
                    source=article.source or "Trade Press",
                    url=article.url,
                    quote=claim["quote"],
                    confidence=claim["confidence"],
                    limitations=claim.get("limitations")
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
    article: Article
    ):
        result = self.extractor.extract(
            text=article.content,
            category="competitive_landscape"
        )
        
        if result.error:
            return []
        
        evidence = []

        for claim in result.claims:
            evidence.append(
                Evidence(
                    claim=claim["claim"],
                    category="competitive_landscape",
                    source=article.source or "Trade Press",
                    url=article.url,
                    quote=claim["quote"],
                    confidence=claim["confidence"],
                    limitations=claim.get("limitations")
                )
            )
        
        return evidence
    
    def create_evidence(
        self,
        claim: str,
        category: str,
        source: str,
        url: str = None,
        quote: str = None,
        confidence: float = 0.5,
        limitations: str = None
    ):

        return Evidence(
            claim=claim,
            category=category,
            source=source,
            url=url,
            quote=quote,
            confidence=confidence,
            limitations=limitations
        )