from backend.llm_interface import call_llm

def run_esg_agent(business_context: str):
    """
    Core ESG reasoning agent.
    Uses structured business context only (no documents).
    """

    prompt = f"""
You are an ESG decision-support agent designed for small and medium-sized businesses.

Your role is NOT to provide generic sustainability advice.
Your role is to:
- Assess ESG maturity
- Identify practical ESG risks
- Prioritize low-cost, high-impact actions
- Explain trade-offs and reasoning clearly

You are NOT a compliance auditor.
You do NOT provide legal guarantees or certifications.

=====================
BUSINESS CONTEXT
=====================
{business_context}

=====================
TASK
=====================
Perform the following steps carefully:

1. Assess the company's CURRENT ESG MATURITY using one of:
   - Low (mostly informal or missing practices)
   - Moderate (some practices exist but are inconsistent or informal)
   - High (well-defined, documented, and consistently followed practices)

2. Identify KEY ESG RISKS across:
   - Environmental (waste, energy, resource use)
   - Governance (roles, accountability, vendor oversight)

3. Determine the NEXT ESG MATURITY MILESTONE the company should aim for.

4. Recommend 3–5 PRIORITY ACTIONS that:
   - Are low-cost and feasible for small businesses
   - Reduce regulatory, operational, or environmental risk
   - Can realistically be executed

5. Explain WHY these actions were prioritized over others.

6. Clearly state ASSUMPTIONS and LIMITATIONS of the advice.

=====================
OUTPUT FORMAT (STRICT)
=====================

### Current ESG Maturity
<Low / Moderate / High> — brief justification

### Key ESG Risks
- Environmental:
- Governance:

### Next ESG Maturity Milestone
<Describe the next realistic improvement stage>

### Priority Actions (Decision-to-Action)
For each action include:
- What
- Who (responsible role)
- Effort (Low / Medium)
- Timeline (Immediate / Short-term / Medium-term)

### Decision Rationale
<Explain why these actions matter most now>

### Assumptions & Limitations
- ...

Do NOT add extra sections.
Do NOT mention laws, certifications, or scores.
"""

    return call_llm(prompt)
