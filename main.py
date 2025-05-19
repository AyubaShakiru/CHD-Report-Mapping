from src.mapper import process_mapping

if __name__ == "__main__":
    input_reports = "data/input/fetal_reports.csv"
    chd_reference = "data/input/chd_reference.csv"
    output_path = "data/output/chd_mapped_output.csv"
    
    process_mapping(input_reports, chd_reference, output_path)
