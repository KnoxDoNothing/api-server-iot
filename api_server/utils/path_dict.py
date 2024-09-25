from pathlib import Path

root_dir = Path(__file__).parents[2]

input_dir = root_dir / "docs"
input_img_dir = input_dir / "images"

output_dir = root_dir / "reports"
output_csv_dir = output_dir / "csv"
output_pdf_dir = output_dir / "pdf"

path_dict = {
    "root_dir": root_dir,
    "input_dir": input_dir,
    "input_img_dir": input_img_dir,
    "output_dir": output_dir,
    "output_csv_dir": output_csv_dir,
    "output_pdf_dir": output_pdf_dir,
}
