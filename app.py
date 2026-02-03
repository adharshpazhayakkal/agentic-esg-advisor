import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# ---------------- Core imports ----------------
from backend.input_handler import validate_inputs
from backend.context_builder import build_esg_context
from backend.agent import run_esg_agent
from backend.agent_rag import run_esg_agent_rag
from backend.retrieval import retrieve_relevant_chunks
from backend.formatter import format_response

# ---------------- App Title ----------------
st.set_page_config(page_title="Agentic ESG Advisor", layout="centered")

st.title("Agentic ESG Advisor for Urban Waste Management & Circular Economy")

tab1, tab2 = st.tabs(["ESG Advisor", "Document-Aware ESG (Advanced)"])

# ============================================================
# TAB 1 — CORE ESG ADVISOR (PRIMARY, STABLE)
# ============================================================
with tab1:
    st.header("ESG Advisor (Input-Based)")
    st.caption("Decision-support for small businesses using agentic reasoning")

    inputs = {
        "business_type": st.selectbox(
            "Business Type",
            ["Manufacturing", "Retail", "Service"]
        ),
        "business_size": st.selectbox(
            "Business Size",
            ["Micro", "Small", "Medium"]
        ),
        "waste_types": st.multiselect(
            "Waste Types",
            ["Organic", "Plastic", "E-waste", "Mixed"]
        ),
        "energy_source": st.selectbox(
            "Energy Source",
            ["Electricity", "Diesel", "Mixed"]
        ),
        "waste_practice": st.selectbox(
            "Waste Handling Practice",
            ["No segregation", "Basic segregation", "Authorized disposal"]
        )
    }

    if st.button("Generate ESG Advisory"):
        try:
            validate_inputs(inputs)
            base_context = build_esg_context(inputs)
            response = run_esg_agent(base_context)
            st.markdown(format_response(response))
        except Exception as e:
            st.error(str(e))


# ============================================================
# TAB 2 — DOCUMENT-AWARE ESG (ADVANCED, OPTIONAL)
# ============================================================
with tab2:
    st.header("Document-Aware ESG (Advanced)")
    st.caption(
        "Ground ESG recommendations using internal company documents. "
        "This is an optional extension and does not replace the core advisor."
    )

    st.subheader("Upload ESG-Relevant Documents (Optional)")

    waste_doc = st.file_uploader(
        "1. Waste Management SOP / Guidelines",
        type=["txt"],
        key="waste_doc"
    )

    energy_doc = st.file_uploader(
        "2. Energy / Operations Note",
        type=["txt"],
        key="energy_doc"
    )

    policy_doc = st.file_uploader(
        "3. Internal Policy / Responsibility Document",
        type=["txt"],
        key="policy_doc"
    )

    vendor_doc = st.file_uploader(
        "4. Vendor / Disposal Agreement (Optional)",
        type=["txt"],
        key="vendor_doc"
    )

    documents = {
        "Waste SOP": waste_doc,
        "Energy Note": energy_doc,
        "Policy Document": policy_doc,
        "Vendor Agreement": vendor_doc
    }

    retrieval_queries = [
        "waste segregation",
        "hazardous waste",
        "waste disposal",
        "diesel generator",
        "energy usage",
        "responsibility",
        "authorization",
        "recycling"
    ]

    retrieved_evidence = []

    for name, doc in documents.items():
        if doc:
            text = doc.read().decode("utf-8")

            chunks = retrieve_relevant_chunks(
                text=text,
                queries=retrieval_queries,
                top_k=2
            )

            if chunks:
                retrieved_evidence.append(f"Evidence from {name}:")
                retrieved_evidence.extend(chunks)

    if retrieved_evidence:
        st.subheader("Retrieved ESG Evidence")
        st.info(
            "The following text snippets were retrieved using sparse (BM25) retrieval "
            "and will be used as supporting evidence."
        )

        for ev in retrieved_evidence:
            st.write(f"- {ev}")

        st.subheader("Generate Document-Grounded ESG Advisory")

        if st.button("Generate ESG Advisory (Document-Grounded)"):
            try:
                # Use the SAME base inputs as Tab 1 for fairness
                validate_inputs(inputs)
                base_context = build_esg_context(inputs)
                evidence_text = "\n".join(retrieved_evidence)

                response = run_esg_agent_rag(
                    business_context=base_context,
                    evidence_context=evidence_text
                )

                st.markdown(format_response(response))

            except Exception as e:
                st.error(str(e))
    else:
        st.warning(
            "No documents uploaded yet. Upload at least one document to enable "
            "document-grounded ESG reasoning."
        )
