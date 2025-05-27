import openai
import pandas as pd
from config.settings import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE
from src.chd_prompt import build_prompt

openai.api_key = OPENAI_API_KEY


def extract_chds_from_report(report_text: str, chd_list: list) -> list:
    """
    Identifies all CHD mentions in the given report text using a list of known CHDs.
    Returns a list of matched CHD names.
    """
    text = str(report_text).lower()
    return [chd for chd in chd_list if chd in text]


def chd_mapping_pipeline(
    reports_csv: str = "fetal_reports.csv",
    reference_csv: str = "ref.csv",
    output_csv: str = "chd_mapped_output.csv"
) -> pd.DataFrame:
    """
    Reads fetal ultrasound reports and a CHD reference file,
    extracts CHDs from each report, maps them to ICD-11 codes,
    and writes the results to a CSV file (one row per CHD per report).
    """

    # Load input files
    reports_df = pd.read_csv(reports_csv)
    ref_df = pd.read_csv(reference_csv)

    # Prepare reference lookup
    ref_df['chd_name_lower'] = ref_df['chd_name'].str.lower()
    chd_dict = ref_df.set_index('chd_name_lower')['icd11_code'].to_dict()
    known_chds = ref_df['chd_name_lower'].tolist()

    expanded_rows = []

    for idx, row in reports_df.iterrows():
        scan_id = row.get('scan_id', f"ROW_{idx}")
        report_text = str(row.get('reports', '')).strip()
        matched_chds = extract_chds_from_report(report_text, known_chds)

        if not matched_chds:
            expanded_rows.append({
                'scan_id': scan_id,
                'report': report_text,
                'chd_name': 'No CHD identified',
                'icd11_code': None
            })
        else:
            for chd in matched_chds:
                original_chd_name = ref_df.loc[ref_df['chd_name_lower'] == chd, 'chd_name'].values[0]
                icd_code = chd_dict.get(chd)
                expanded_rows.append({
                    'scan_id': scan_id,
                    'report': report_text,
                    'chd_name': original_chd_name,
                    'icd11_code': icd_code
                })

    output_df = pd.DataFrame(expanded_rows)
    output_df.to_csv(output_csv, index=False)
    print(f"✅ Output saved to: {output_csv}")
    return output_df


# Example usage
if __name__ == "__main__":
    df = chd_mapping_pipeline(
        reports_csv="fetal_reports.csv",
        reference_csv="ref.csv",
        output_csv="chd_mapped_output.csv"
    )
    print(df.head())
