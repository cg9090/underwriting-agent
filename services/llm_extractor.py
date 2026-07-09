import json

from llm.claude import LLMClient
from models.extraction import ExtractionResult


class LLMEvidenceExtractor:

    def __init__(self):
        self.client = LLMClient()


    def extract(
        self,
        text: str,
        category: str
    ):

        prompt = f"""
You are an evidence extraction system.

Extract up to 5 of the most important factual claims from the following source.

Rules:
- Only use information explicitly stated in the text.
- Do not make assumptions.
- Each claim must be supported by a quote.
- Return JSON only.

For each claim provide:

claim:
A concise factual statement

quote:
The exact supporting text

confidence:
A number between 0 and 1

limitations:
Any reason the evidence may be incomplete

Return ONLY valid JSON.

The output must be an array.

Each item must contain:

{{
  "claim": string,
  "quote": string,
  "confidence": number,
  "limitations": string
}}

Do not include:
- markdown
- explanations
- commentary
- code fences


Category:
{category}


Source text:
{text}
"""

        try:

            response = self.client.generate(prompt=prompt)

        except Exception as e:
            return ExtractionResult(
                error="LLM call failed: " + str(e)
            )
        
        cleaned = response.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "", 1)

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        try:

            claims = json.loads(cleaned)
            claims = claims[:5]
            return ExtractionResult(
                claims=claims
            )

        except json.JSONDecodeError:

            return ExtractionResult(
                error="LLM returned invalid JSON"
            )