def build_esg_context(inputs):
    context = f"""
Business Profile:
- Business Type: {inputs['business_type']}
- Business Size: {inputs['business_size']}

Environmental Factors:
- Waste Types: {inputs['waste_types']}
- Waste Handling Practice: {inputs['waste_practice']}
- Energy Source: {inputs['energy_source']}

Focus Area:
Urban waste management and circular economy readiness.
"""
    return context
