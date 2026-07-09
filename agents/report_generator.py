import os

from anthropic import Anthropic
from dotenv import load_dotenv

from models.research import ResearchState

load_dotenv()


class ReportGenerator:

    def __init__(self):

        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def generate(
        self,
        state: ResearchState
    ):

        evidence = ""

        for item in state.evidence:

            evidence += f"""
Category: {item.category}

Claim:
{item.claim}

Source:
{item.source}

Confidence:
{item.confidence}


URL:
{item.url}

------------------------------
"""

        prompt = f"""
You are an experienced commercial underwriting analyst.

Your task is to produce an underwriting intelligence report.

Only use the evidence provided below.

If there is insufficient evidence for a conclusion, explicitly say so.

Every factual statement should reference its source.

Company

{state.company.company_name}

Evidence

{evidence}

Generate the report with the following sections.

# Business Model Summary

Explain:

- What the company does
- How it makes money
- Who its customers are

State confidence.

---

# Competitive Landscape

Assess

- Degree of competition
- Why competition matters
- Relevant competitors
- Geographic market

State confidence.

---

# Company Quality Signals

Summarise

- Positive signals
- Negative signals
- Trade press
- Customer sentiment if available

State confidence.

Mention conflicting evidence.

---

# Sources

List all sources used.
"""

        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text