def validate_inputs(inputs):
    required = [
        "business_type",
        "business_size",
        "waste_types",
        "energy_source",
        "waste_practice"
    ]

    for field in required:
        if field not in inputs or not inputs[field]:
            raise ValueError(f"Missing input: {field}")

    return True
