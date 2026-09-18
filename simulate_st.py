import sys
from unittest.mock import MagicMock
sys.modules['streamlit'] = MagicMock()
sys.modules['streamlit.components.v1'] = MagicMock()

import app

# Mock uploaded files
class MockFile:
    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[-1]
        with open(path, 'rb') as f:
            self.content = f.read()
        self.pos = 0
    
    def seek(self, pos):
        self.pos = pos
        
    def read(self, *args):
        return self.content[self.pos:]

import glob
f1 = MockFile('/Users/hernanbrito/.gemini/antigravity/brain/a8d9fcca-24d8-48aa-b10b-158ce4b415d0/.user_uploaded/media_1789607826813.pdf')
f2 = MockFile('/Users/hernanbrito/.gemini/antigravity/brain/a8d9fcca-24d8-48aa-b10b-158ce4b415d0/.user_uploaded/media_1789607826871.pdf')

from processor2 import extract_all_text, process_data
text = extract_all_text([f1, f2], "")
print("Len text:", len(text))
res, _, _ = process_data(text, 950, 37900*13.5, 200000, 200000, 200000)
c = 0
for k, v in res.items():
    if v > 0:
        print(f"{k}: {v}")
        c += 1
print("Total found:", c)
