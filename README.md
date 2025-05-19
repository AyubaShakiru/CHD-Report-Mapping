# CHD-Report-Mapping
A mapping of CHD types with the corresponding ICD11 code based on the clinician report.

# 🫀 CHD Report Mapping Tool

This project provides a Python-based pipeline to extract Congenital Heart Disease (CHD) mentions from clinician-written fetal ultrasound reports and map them to ICD-11 codes using a verified reference list. The tool is built with clinical accuracy in mind, minimizing hallucinations by leveraging GPT with strict prompting and reference matching.

---

## 📌 Overview

- Extracts CHD diagnoses from free-text reports
- Uses a structured reference list to ensure only medically valid CHDs are included
- Maps each diagnosis to its corresponding ICD-11 code and reference number
- Outputs clean, audit-ready CSV files for further annotation or analysis

---

## 🧱 Project Structure

chd_icd_mapping_project/
├── data/
│ ├── input/
│ │ ├── fetal_reports.csv # Input: scan_id, report
│ │ └── chd_reference.csv # Input: chd_name, icd11_code, reference_number
│ └── output/
│ └── chd_mapped_output.csv # Output: mapped CHDs per report
├── src/
│ ├── init.py
│ ├── chd_prompt.py # Constructs hallucination-resistant GPT prompts
│ ├── mapper.py # Core processing logic
├── config/
│ └── settings.py # OpenAI API key and model settings
├── main.py # Entrypoint to run the program
├── requirements.txt
└── README.md


---

## ⚙️ Requirements

- Python 3.8+
- OpenAI Python SDK
- `pandas`, `python-dotenv`

Install dependencies:
```bash
- pip install -r requirements.txt


## 1. 🔑 Setup
Add your OpenAI API key to a .env file in the root directory:
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxx


## 2. Prepare your input files:

fetal_reports.csv with columns:

scan_id

report

chd_reference.csv with columns:

chd_name

icd11_code

reference_number

## 🚀 Run the Tool
python main.py

This will read the reports and reference file, query GPT with structured prompts, and produce a mapped output file at:

data/output/chd_mapped_output.csv

Each row in the output will contain:

scan_id

report

chd_name (or "CHD type not found in reference")

icd11_code

reference_number

✅ Features

🔒 Hallucination-resistant design — GPT can only choose from your reference list

📄 Maintains original reports alongside mapped outputs

⚠️ Flags unmatched CHDs explicitly for review

💡 Easily extendable for semi-supervised labeling or annotation pipelines


## 👨‍🔬 Collaborators

Shakiru Ayuba – PhD Researcher, Birmingham City University

Prof. Bilal Muhammad – Research Supervisor


## 📄 License
This codebase is provided for academic research and educational use only. Contact the author for other uses or distribution.


## 📬 Contact
For feedback or collaboration inquiries, please reach out via:

📧 [shakiru.ayuba@mail.bcu.ac.uk]
🔗 https://github.com/AyubaShakiru
