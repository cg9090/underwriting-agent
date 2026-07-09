import os

from dotenv import load_dotenv

from models.research import ResearchState

from llm.claude import LLMClient

load_dotenv()


class ReportGenerator:

    def __init__(self):

        self.client = LLMClient()

    def generate(
        self,
        state: ResearchState,
        evidence_summary: dict
    ):

        evidence = ""

        for item in state.evidence:

            evidence += f"""
Category: {item.category}

Claim:
{item.claim}

Quote:
{item.quote}

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

IMPORTANT:
The evidence strength summary represents how confident the system is in each section.
Do not make strong conclusions where evidence strength is low.
Explicitly mention limitations and uncertainty.

Evidence Strength Summary:

{evidence_summary}

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

List all sources used including the URLs
"""

        response = self.client.generate(prompt=prompt)

        return response