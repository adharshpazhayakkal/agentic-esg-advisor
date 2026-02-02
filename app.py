import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from backend.input_handler import validate_inputs
from backend.context_builder import build_esg_context
from backend.agent import run_esg_agent
from backend.formatter import format_response

st.title("Agentic ESG Advisor for Urban Waste Management")

inputs = {
    "business_type": st.selectbox("Business Type", ["Manufacturing", "Retail", "Service"]),
    "business_size": st.selectbox("Business Size", ["Micro", "Small", "Medium"]),
    "waste_types": st.multiselect("Waste Types", ["Organic", "Plastic", "E-waste", "Mixed"]),
    "energy_source": st.selectbox("Energy Source", ["Electricity", "Diesel", "Mixed"]),
    "waste_practice": st.selectbox(
        "Waste Handling Practice",
        ["No segregation", "Basic segregation", "Authorized disposal"]
    )
}

if st.button("Generate ESG Advisory"):
    try:
        validate_inputs(inputs)
        context = build_esg_context(inputs)
        response = run_esg_agent(context)
        st.markdown(format_response(response))
    except Exception as e:
        st.error(str(e))
