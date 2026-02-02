from backend.llm_interface import call_llm

def run_esg_agent(context):
    prompt = f"""
You are an ESG decision-support agent for small businesses.

Context:
{context}

Tasks:
1. Classify ESG readiness as Low, Moderate, or High
2. Identify key waste and governance risks
3. Recommend 3–5 low-cost, high-impact actions
4. Explain why each action matters
5. Avoid legal or certification claims

Respond in clear sections.
"""
    return call_llm(prompt)
