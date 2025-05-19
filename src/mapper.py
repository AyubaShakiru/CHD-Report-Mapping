import openai
import pandas as pd
from config.settings import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE
from src.chd_prompt import build_prompt

openai.api_key = OPENAI_API_KEY


def get_chds_from_gpt(report, known_chds):
    """Send the report and known CHDs to GPT and return raw CHD list."""
    try:
        prompt = build_prompt(report, known_chds)
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a clinical assistant for CHD detection and ICD-11 coding."},
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"


def process_mapping(input_report_path, chd_reference_path, output_path):
    # Load clinician reports and CHD reference list
    try:
        reports_df = pd.read_csv(input_report_path)
        ref_df = pd.read_csv(chd_reference_path)
    except Exception as e:
        print(f"❌ Error reading input files: {e}")
        return

    # Build a dictionary for reference CHDs and a list of known CHDs
    ref_dict = ref_df.set_index('chd_name').to_dict('index')
    known_chds = ref_df['chd_name'].tolist()

    output_rows = []

    for idx, row in reports_df.iterrows():
        scan_id = row.get('scan_id')
        report = row.get('report', '').strip()

        if not report:
            output_rows.append({
                'scan_id': scan_id,
                'report': "",
                'chd_name': "No report provided",
                'icd11_code': None,
                'reference_number': None
            })
            continue

        gpt_output = get_chds_from_gpt(report, known_chds)

        # Extract CHDs from GPT response
        matched_chds = [
            line.strip() for line in gpt_output.split('\n')
            if line.strip() and "no chd" not in line.lower()
        ]

        if not matched_chds:
            output_rows.append({
                'scan_id': scan_id,
                'report': report,
                'chd_name': "No CHD identified",
                'icd11_code': None,
                'reference_number': None
            })
        else:
            for chd in matched_chds:
                chd_clean = chd.strip()
                if chd_clean in ref_dict:
                    output_rows.append({
                        'scan_id': scan_id,
                        'report': report,
                        'chd_name': chd_clean,
                        'icd11_code': ref_dict[chd_clean]['icd11_code'],
                        'reference_number': ref_dict[chd_clean]['reference_number']
                    })
                else:
                    output_rows.append({
                        'scan_id': scan_id,
                        'report': report,
                        'chd_name': f"CHD type not found in reference: {chd_clean}",
                        'icd11_code': None,
                        'reference_number': None
                    })

    # Save results to output CSV
    try:
        out_df = pd.DataFrame(output_rows)
        out_df.to_csv(output_path, index=False)
        print(f"✅ ICD mapping output saved to: {output_path}")
    except Exception as e:
        print(f"❌ Failed to save output file: {e}")
