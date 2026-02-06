import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# ---------------- Backend imports ----------------
from backend.input_handler import validate_inputs
from backend.context_builder import build_esg_context
from backend.agent import run_esg_agent
from backend.agent_rag import run_esg_agent_rag
from backend.retrieval import retrieve_relevant_chunks
from backend.formatter import format_response

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="ESG Decision Support System",
    layout="centered"
)

# ---------------- Title ----------------
st.title("ESG Decision-to-Action Advisory System")
st.caption(
    "A lightweight internal ESG decision-support tool to assess maturity, "
    "identify risks, and prioritize practical actions for small and medium-sized organizations."
)

tab1, tab2 = st.tabs([
    "ESG Assessment",
    "Document-Grounded ESG Review"
])

# ============================================================
# TAB 1 — ESG ASSESSMENT (CORE SYSTEM)
# ============================================================
with tab1:
    st.header("Organizational Context")
    st.caption(
        "Provide basic operational context. This assessment is designed to be completed "
        "in under two minutes."
    )

    inputs = {
        "business_type": st.selectbox(
            "Primary Business Activity",
            ["Manufacturing", "Retail", "Service"]
        ),
        "business_size": st.selectbox(
            "Organization Size",
            ["Micro", "Small", "Medium"]
        ),
        "waste_types": st.multiselect(
            "Waste Streams Generated",
            ["Organic", "Plastic", "E-waste", "Mixed"],
            help="Select all waste categories generated during normal operations"
        ),
        "energy_source": st.selectbox(
            "Primary Energy Source",
            ["Electricity", "Diesel", "Mixed"]
        ),
        "waste_practice": st.selectbox(
            "Waste Handling Maturity",
            [
                "No formal segregation",
                "Basic or informal segregation",
                "Authorized and documented disposal"
            ]
        )
    }

    if st.button("Generate ESG Action Plan"):
        try:
            validate_inputs(inputs)
            base_context = build_esg_context(inputs)
            response = run_esg_agent(base_context)
            st.markdown(format_response(response))
        except Exception as e:
            st.error(str(e))

    st.caption(
        "This system provides ESG decision-support and prioritization guidance. "
        "It does not perform regulatory audits or certification."
    )

# ============================================================
# TAB 2 — DOCUMENT-GROUNDED ESG REVIEW (EXTENSION)
# ============================================================
with tab2:
    st.header("Evidence-Grounded ESG Review")
    st.caption(
        "Optional review using internal operational documents to validate declared practices. "
        "Missing or unclear documentation is treated as an ESG risk signal."
    )

    st.subheader("Internal Operational Documents (Optional)")

    waste_doc = st.file_uploader(
        "Waste Management SOP or Operational Guidelines",
        type=["txt"],
        key="waste_doc"
    )

    energy_doc = st.file_uploader(
        "Energy or Operations Notes",
        type=["txt"],
        key="energy_doc"
    )

    policy_doc = st.file_uploader(
        "Internal Policy or Responsibility Document",
        type=["txt"],
        key="policy_doc"
    )

    vendor_doc = st.file_uploader(
        "Vendor or Disposal Agreement (Optional)",
        type=["txt"],
        key="vendor_doc"
    )

    documents = {
        "Waste SOP": waste_doc,
        "Energy Notes": energy_doc,
        "Policy Document": policy_doc,
        "Vendor Agreement": vendor_doc
    }

    retrieval_queries = [
        "waste segregation",
        "hazardous waste",
        "waste disposal",
        "recycling",
        "diesel generator",
        "energy usage",
        "responsibility",
        "authorization"
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
        st.subheader("Retrieved Evidence")
        st.info(
            "The following excerpts were retrieved using controlled keyword-based retrieval "
            "and are used as supporting evidence for ESG reasoning."
        )

        for ev in retrieved_evidence:
            st.write(f"- {ev}")

        if st.button("Generate Evidence-Grounded ESG Action Plan"):
            try:
                # Safe defaults for document-grounded mode
                doc_inputs = inputs.copy()
                if not doc_inputs["waste_types"]:
                    doc_inputs["waste_types"] = ["Mixed"]

                validate_inputs(doc_inputs)
                base_context = build_esg_context(doc_inputs)
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
            "evidence-grounded ESG reasoning."
        )
