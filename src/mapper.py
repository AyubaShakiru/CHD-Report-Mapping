import openai
import pandas as pd
from config.settings import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE
from src.chd_prompt import build_prompt

openai.api_key = OPENAI_API_KEY


import pandas as pd

def analyze_chds_in_report(report_text: str, ref_df: pd.DataFrame):
    """
    Classify CHDs in a report as 'asserted' (explicitly stated) or 'inferred' (discussed but not clearly diagnosed).
    """
    asserted_chds = []
    inferred_chds = []
    text = str(report_text).lower()

    for _, row in ref_df.iterrows():
        chd_lower = row['chd_name'].lower()

        # Asserted patterns
        if any(phrase in text for phrase in [
            f"diagnosed with {chd_lower}",
            f"confirmed {chd_lower}",
            f"has {chd_lower}",
            f"presence of {chd_lower}",
            f"evidence of {chd_lower}"
        ]):
            asserted_chds.append((row['chd_name'], row['icd11_code']))

        # Inferred patterns (CHD name is present but not strongly asserted)
        elif chd_lower in text:
            inferred_chds.append((row['chd_name'], row['icd11_code']))

    return asserted_chds, inferred_chds


def extended_chd_mapping_pipeline(
    reports_csv: str,
    reference_csv: str,
    output_csv: str
) -> pd.DataFrame:
    """
    Process fetal ultrasound reports and classify CHDs as asserted or inferred,
    mapping to ICD-11 codes and saving the result to a CSV file.
    """
    reports_df = pd.read_csv(reports_csv)
    ref_df = pd.read_csv(reference_csv)

    results = []

    for idx, row in reports_df.iterrows():
        scan_id = row.get('scan_id', f"ROW_{idx}")
        report_text = str(row.get('reports', '')).strip()

        asserted, inferred = analyze_chds_in_report(report_text, ref_df)

        results.append({
            "scan_id": scan_id,
            "report": report_text,
            "CHD_Asserted": "; ".join([x[0] for x in asserted]) if asserted else "None",
            "CHD_Inferred": "; ".join([x[0] for x in inferred]) if inferred else "None",
            "ICD11_Codes_Asserted": "; ".join([x[1] for x in asserted]) if asserted else "None",
            "ICD11_Codes_Inferred": "; ".join([x[1] for x in inferred]) if inferred else "None"
        })

    output_df = pd.DataFrame(results)
    output_df.to_csv(output_csv, index=False)
    print(f"✅ Output saved to: {output_csv}")
    return output_df


# Example usage
if __name__ == "__main__":
    reports_file = "fetal_reports.csv"
    reference_file = "ref.csv"
    output_file = "extended_chd_analysis.csv"

    df = extended_chd_mapping_pipeline(reports_file, reference_file, output_file)
    print(df.head())
