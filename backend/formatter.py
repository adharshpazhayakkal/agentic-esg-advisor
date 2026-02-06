def format_response(response: str) -> str:
    """
    Formats ESG agent output into a clean, enterprise-style advisory
    suitable for decision-makers.
    """

    lines = response.split("\n")
    formatted = []

    for line in lines:
        line = line.strip()

        # Headings
        if line.startswith("### "):
            formatted.append(f"\n## {line.replace('### ', '')}\n")

        # Bullet points
        elif line.startswith("- "):
            formatted.append(f"- {line[2:]}")

        # Numbered actions
        elif line[:2].isdigit() and line[2] == ".":
            formatted.append(f"\n**{line}**")

        # Labels inside actions
        elif line.lower().startswith("what"):
            formatted.append(f"**What:** {line.split(':', 1)[-1].strip()}")

        elif line.lower().startswith("who"):
            formatted.append(f"**Who:** {line.split(':', 1)[-1].strip()}")

        elif line.lower().startswith("effort"):
            formatted.append(f"**Effort:** {line.split(':', 1)[-1].strip()}")

        elif line.lower().startswith("timeline"):
            formatted.append(f"**Timeline:** {line.split(':', 1)[-1].strip()}")

        # Empty lines
        elif line == "":
            formatted.append("")

        # Default text
        else:
            formatted.append(line)

    # Join and add a professional footer
    formatted_output = "\n".join(formatted)

    formatted_output += """
---
**Note:**  
This ESG advisory is a decision-support output based on provided inputs and available
document evidence. It highlights priority actions and risks but does not constitute
legal, regulatory, or certification advice.
"""

    return formatted_output
