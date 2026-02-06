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
    page_title="ESG Decision-to-Action System",
    layout="centered"
)

# ---------------- Title & Positioning ----------------
st.title("ESG Decision-to-Action Advisory System")
st.caption(
    "Internal ESG decision support for small and medium-sized organizations. "
    "This system assesses ESG maturity, identifies risks, and prioritizes "
    "practical actions across waste management, energy use, and governance."
)

# ---------------- Tabs ----------------
tab1, tab2 = st.tabs([
    "ESG Assessment & Action Planning",
    "Evidence-Grounded ESG Review"
])

# ============================================================
# TAB 1 — ESG ASSESSMENT & ACTION PLANNING
# ============================================================
with tab1:
    st.header("Organizational ESG Context")
    st.caption(
        "Provide high-level operational context. Inputs are intentionally minimal "
        "to reduce reporting burden while enabling meaningful ESG reasoning."
    )

    # ---- Inputs (Professional Controls) ----
    business_type = st.radio(
        "Primary Operational Sector",
        ["Manufacturing", "Retail", "Service"],
        horizontal=True
    )

    business_size = st.radio(
        "Organization Scale",
        ["Micro (1–10 employees)", "Small (11–50 employees)", "Medium (51–250 employees)"]
    )

    waste_types = st.multiselect(
        "Primary Waste Streams Generated",
        ["Organic", "Plastic", "E-waste", "Mixed"],
        help="Select all waste categories generated during normal operations"
    )

    energy_sources = st.multiselect(
        "Primary Energy Sources",
        ["Grid Electricity", "Diesel Generator", "Renewable (On-site / Off-site)"],
        default=["Grid Electricity"]
    )

    waste_practice = st.select_slider(
        "Waste Handling Maturity",
        options=[
            "No formal practices",
            "Informal or partial practices",
            "Standardized and documented practices"
        ]
    )

    esg_ownership = st.radio(
        "ESG Responsibility Ownership",
        [
            "No defined ownership",
            "Handled informally by operations",
            "Assigned to a specific role or team"
        ]
    )

    # ---- Map UI inputs to backend-compatible structure ----
    inputs = {
        "business_type": business_type,
        "business_size": business_size.split(" ")[0],  # Micro / Small / Medium
        "waste_types": waste_types,
        "energy_source": "Mixed" if len(energy_sources) > 1 else energy_sources[0],
        "waste_practice": waste_practice,
        "esg_ownership": esg_ownership
    }

    # ---- Action Button ----
    if st.button("Generate ESG Action Plan"):
        try:
            validate_inputs(inputs)
            base_context = build_esg_context(inputs)
            response = run_esg_agent(base_context)
            st.markdown(format_response(response))
        except Exception as e:
            st.error(str(e))

    st.caption(
        "This system provides ESG decision support and prioritization guidance. "
        "It does not perform regulatory audits or certification."
    )

# ============================================================
# TAB 2 — EVIDENCE-GROUNDED ESG REVIEW
# ============================================================
with tab2:
    st.header("Evidence-Grounded ESG Review")
    st.caption(
        "Optional review using internal operational documents to validate declared practices. "
        "Document evidence is used to strengthen or flag ESG risk assumptions."
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
            "The following excerpts were retrieved using controlled, keyword-based retrieval "
            "and are used as supporting evidence for ESG reasoning."
        )

        for ev in retrieved_evidence:
            st.write(f"- {ev}")

        if st.button("Generate Evidence-Grounded ESG Action Plan"):
            try:
                # ---- Safe defaults for document-grounded mode ----
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

    st.caption(
        "Document evidence is treated as supportive input. "
        "Missing or unclear documentation is considered an ESG risk signal."
    )
