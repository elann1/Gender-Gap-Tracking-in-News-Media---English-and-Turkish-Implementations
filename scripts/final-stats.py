file_path = ""

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()


paragraphs = [p for p in text.split("\n\n") if p.strip()]
paragraph_count = len(paragraphs)

print(f"Total paragraphs: {paragraph_count}")

char_count = len(text)

print(f"Total characters: {char_count}")

import pandas as pd
excel_path = ""
df= pd.read_excel(excel_path)
df.head()

