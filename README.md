# Agentic ESG Advisor for Urban Waste Management & Circular Economy

## Overview
This project is an **Agentic ESG Decision-Support System** designed to help small and medium-sized businesses (SMBs) understand their ESG readiness and prioritize **low-cost, high-impact sustainability actions**, with a primary focus on **urban waste management and circular economy practices**.

Unlike traditional ESG tools that emphasize reporting, certification, or complex analytics, this system focuses on **practical decision-making, action prioritization, and explainability**, making ESG adoption accessible for resource-constrained businesses.

---

## Problem Statement
Small businesses often struggle to adopt ESG practices due to:
- Limited awareness of ESG requirements
- Informal waste management and disposal practices
- High cost and complexity of existing ESG tools
- Lack of clarity on which sustainability actions should be prioritized first

As a result, ESG adoption becomes reactive rather than proactive, increasing regulatory, operational, and reputational risks.

---

## Proposed Solution
The proposed solution is an **Agentic ESG Advisor** that:
- Interprets basic business information
- Builds contextual ESG understanding
- Reasons over sustainability risks
- Prioritizes actionable recommendations
- Explains *why* each action matters

The system functions as a **decision-support engine**, not a chatbot or prediction model.

---

## Key Features
- Agentic AI-based reasoning (decision-oriented, not rule-based)
- Focus on urban waste management and circular economy
- Cost-aware and practical ESG recommendations
- Explainable outputs to build user trust
- Lightweight, deployable Streamlit application

---

## Input Parameters
The system intentionally uses a **minimal but high-signal input set** to reduce friction for users:

- **Business Type:** Manufacturing / Retail / Service  
- **Business Size:** Micro / Small / Medium  
- **Waste Types:** Organic / Plastic / E-waste / Mixed  
- **Energy Source:** Electricity / Diesel / Mixed  
- **Waste Handling Practice:** No segregation / Basic segregation / Authorized disposal  

This input design balances usability with meaningful ESG reasoning.

---

## Agentic AI Architecture

### What Makes This System Agentic?
The system does not simply generate responses. Instead, it follows a **structured reasoning workflow** similar to how a human ESG consultant would analyze a business context and recommend prioritized actions.

### Multi-Layer System Architecture

Each layer has a clearly defined responsibility, ensuring modularity, transparency, and robustness.

---

## Backend Workflow

1. **User Input Collection**  
   Business information is collected through a Streamlit-based interface.

2. **Input Validation and Preprocessing**  
   Inputs are validated for completeness and normalized into structured categories.

3. **ESG Context Construction**  
   The system builds an internal ESG context summarizing environmental and governance exposure.

4. **Agentic ESG Reasoning**  
   A GenAI-based agent evaluates ESG readiness, identifies key risks, and prioritizes actions based on cost, feasibility, and sustainability impact.

5. **Explainable Output Generation**  
   Results are presented in a structured and readable format to support informed decision-making.

---

## Technology Stack
- **Frontend:** Streamlit  
- **Backend:** Python  
- **Agentic Reasoning Engine:** Google Gemini (free tier)  
- **Deployment:** Streamlit Community Cloud  
- **Version Control:** GitHub  

The architecture also supports switching to open-source models (e.g., Mistral) without major code changes.

---

## Expected Impact
- Improved ESG awareness among small and medium-sized businesses  
- Better waste management and circular economy adoption  
- Reduced regulatory and operational risks  
- Cost-effective sustainability decision-making  
- Practical ESG readiness for future growth  

---

## Why This Project is Unique
- Focuses on **decision support**, not ESG reporting
- Uses **agentic reasoning** instead of static rules
- Designed specifically for **small businesses**
- Emphasizes **low-cost, high-impact actions**
- Fully deployable with minimal infrastructure

---

## Deployment
The application is deployed using **Streamlit Community Cloud**.  
Any updates pushed to the GitHub repository are automatically reflected in the deployed application.

---

## Disclaimer
This system provides ESG awareness and decision support only.  
It does **not** offer legal advice, certification, or regulatory compliance guarantees.

---

## Authors
Developed as part of the **Internal Capacity Building Program (ICBP 3.0)**  
Focus Area: **Sustainability – Urban Waste Management & Circular Economy**
