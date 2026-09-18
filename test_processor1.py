from processor import process_data, extract_text_from_pdf
import glob

pdf_files = glob.glob("/Users/hernanbrito/.gemini/antigravity/brain/a8d9fcca-24d8-48aa-b10b-158ce4b415d0/.user_uploaded/*.pdf")
raw_text = ""
for f in pdf_files:
    with open(f, 'rb') as file_obj:
        raw_text += extract_text_from_pdf(file_obj) + "\n"

res, _, _ = process_data(raw_text, 950, 37900*13.5, 200000, 200000, 200000)
count = 0
for k, v in res.items():
    if v > 0:
        count += 1
        print(f"{k}: {v}")
print("TOTAL:", count)
