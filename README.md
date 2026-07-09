## System Design Note

### Architectural Approach

The system is designed as an evidence-driven underwriting research agent. The main design principle is to separate **information gathering**, **evidence extraction**, and **report generation** so that conclusions can be traced back to the underlying sources.

The workflow follows these stages:

1. **Company Resolution**
   - The system first identifies the target company using Companies House data.
   - If a company name is ambiguous, the user is asked to select the correct company rather than automatically choosing the first result.
   - This avoids incorrect research being performed on the wrong entity.

2. **Evidence Collection**
   - Information is gathered from multiple sources:
     - Companies House for company registration and legal information
     - Official company websites for products and services
     - Trade press for reputation and market signals
     - Web sources for competitive landscape research

3. **Evidence Normalisation**
   - All findings are converted into a common `Evidence` model containing:
     - Claim
     - Category
     - Source
     - URL (where available)
     - Supporting quote (where available)
     - Confidence score
     - Limitations

   This allows different sources to be compared consistently and ensures that the final report is grounded in retrieved information.

4. **Assessment and Report Generation**
   - Before generating a final report, the system assesses whether sufficient evidence exists for each section:
     - Business model
     - Competitive landscape
     - Quality signals

   - The LLM is instructed to only use the provided evidence and explicitly highlight uncertainty or missing information.

---

### Key Design Decisions

#### Evidence-first architecture

Rather than asking an LLM to research and write a report directly, the system separates research from reasoning.

This reduces hallucination risk because the model is only responsible for synthesising previously collected evidence rather than generating unsupported facts.

#### Human-in-the-loop company selection

Company names can be ambiguous. Automatically selecting the first search result could result in analysing the wrong business.

The system therefore requires user confirmation when multiple companies match a search query.

#### Confidence and uncertainty handling

The system does not assume all evidence is equally reliable.

Examples:
- Companies House provides high-confidence legal information.
- Trade press provides useful reputation signals but may contain publication bias.
- Search results provide weaker competitive signals.

Confidence scores and evidence limitations are included to avoid over-generalisation.

#### Modular source architecture

External sources are isolated behind separate clients:

- Company House client
- Website scraper
- Trade press searcher
- Competition researcher
- LLM client

This allows sources to be replaced or extended without changing the main workflow.

---

### What I Would Do Differently With More Time

#### 1. Improve source quality and reliability

The current system relies heavily on web search and scraping. With more time I would integrate additional structured sources, such as:

- Financial data providers
- Regulatory databases
- Customer review platforms
- Industry-specific market datasets

This would improve evidence quality and reduce reliance on unstructured web content.

#### 2. Add stronger evidence ranking

Currently evidence is scored using confidence values. A future version would rank evidence based on:

- Source reliability
- Recency
- Independence of source
- Agreement between multiple sources

This would allow the system to prioritise the strongest signals.

#### 3. Introduce more advanced workflow orchestration

The current workflow uses a deterministic pipeline. A future version could use an agent orchestration framework to allow dynamic decisions such as:

- Whether more research is required
- Which sources to query next
- When evidence is sufficient to generate a report
- How to recover from failed searches

#### 4. Improve evaluation and monitoring

A production version would include:

- Automated tests against known companies
- Tracking of unsupported claims
- Logging of evidence used for each report conclusion
- Human feedback loops to improve report quality

---

### Summary

The system prioritises trustworthy underwriting analysis over simply generating a company summary. By separating evidence collection from report generation and explicitly modelling confidence and uncertainty, the design aims to produce reports that are transparent, traceable, and suitable for decision support.