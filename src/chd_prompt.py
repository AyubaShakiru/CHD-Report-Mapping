def build_prompt(report_text: str, known_chds: list) -> str:
    """
    Builds a structured, hallucination-resistant prompt for GPT
    to extract CHDs strictly from a reference list.
    """
    chd_list_text = "\n".join(f"- {chd}" for chd in known_chds)

    return f"""You are a clinical reasoning assistant trained to extract Congenital Heart Disease (CHD) diagnoses from fetal ultrasound reports.

You are given:
1. A list of known CHD types (based on an expert-verified reference).
2. A fetal ultrasound report written by a clinician.

Your task is to:
- Identify only CHD types that are clearly and explicitly stated in the report.
- Use only CHDs from the provided list.
- Do NOT guess or infer any diagnosis.
- Do NOT hallucinate or make assumptions beyond what is stated.
- Return only the CHD names that appear in the list below.

If no CHD is found in the report, return exactly:
No CHD identified

### List of known CHDs:
{chd_list_text}

### Report:
\"\"\"{report_text}\"\"\"

### Output Format:
If CHDs are found, list one per line:
CHD Name 1  
CHD Name 2  
...

If no CHD is found, return:
No CHD identified
"""
