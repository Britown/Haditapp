import PyPDF2
from processor2 import process_data

raw_text = ""
with open('/Users/hernanbrito/.gemini/antigravity/brain/a8d9fcca-24d8-48aa-b10b-158ce4b415d0/.user_uploaded/media_1789607826813.pdf', 'rb') as f1:
    reader = PyPDF2.PdfReader(f1)
    for p in reader.pages:
        t = p.extract_text()
        if t: raw_text += t + "\n"

with open('/Users/hernanbrito/.gemini/antigravity/brain/a8d9fcca-24d8-48aa-b10b-158ce4b415d0/.user_uploaded/media_1789607826871.pdf', 'rb') as f2:
    reader = PyPDF2.PdfReader(f2)
    for p in reader.pages:
        t = p.extract_text()
        if t: raw_text += t + "\n"

print("Len:", len(raw_text))
res, _, _ = process_data(raw_text, 950, 37900*13.5, 200000, 200000, 200000)
c = 0
for k, v in res.items():
    if v > 0:
        c += 1
        print(f"{k}: {v}")
print("Total:", c)
