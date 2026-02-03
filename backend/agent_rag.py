from backend.llm_interface import call_llm

def run_esg_agent_rag(business_context, evidence_context):
    """
    business_context: ESG context from structured user inputs
    evidence_context: Retrieved document chunks (BM25-based)
    """

    prompt = f"""
You are an ESG decision-support agent for small and medium-sized businesses.

This is a DOCUMENT-GROUNDED advisory mode.
You must reason using BOTH:
- Business context provided by the user
- Retrieved evidence from internal documents

=====================
BUSINESS CONTEXT
=====================
{business_context}

=====================
DOCUMENT EVIDENCE (Retrieved)
=====================
The following snippets were retrieved from internal company documents.
They may be incomplete or informal.
Use them ONLY as supporting evidence.

{evidence_context}

=====================
TASK
=====================
1. Assess ESG readiness as one of: Low / Moderate / High
2. Identify ESG risks related to waste management, energy use, and governance
3. Recommend 3–5 low-cost, high-impact ESG actions
4. Explain WHY each action matters
5. Explicitly mention gaps if evidence is missing or weak

=====================
OUTPUT FORMAT (STRICT)
=====================

### ESG Readiness
<Low / Moderate / High>

### Key ESG Risks
- ...

### Priority Actions
1. ...
2. ...
3. ...

### Why These Actions Matter
- ...

Do NOT add extra sections.
Do NOT mention laws or certifications.
"""

    return call_llm(prompt)
