from processor2 import process_data, extract_text_from_pdf
import os
import glob

pdf_files = glob.glob("/Users/hernanbrito/.gemini/antigravity/brain/a8d9fcca-24d8-48aa-b10b-158ce4b415d0/.user_uploaded/*.pdf")
raw_text = ""
for f in pdf_files:
    print(f"Reading {f}")
    with open(f, 'rb') as file_obj:
        raw_text += extract_text_from_pdf(file_obj) + "\n"

print("Total length of extracted text:", len(raw_text))

res, fechas, un = process_data(raw_text, 950, 37900*13.5, 200000, 200000, 200000)
for k, v in res.items():
    if v > 0:
        print(f"{k}: {v}")
