#English Corpus Article Sampling

import os
import re

base_dir = ""  
section_folders = [os.path.join(base_dir, folder) for folder in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, folder))]

sampled_articles = []

for folder in section_folders:
    files = sorted(os.listdir(folder))  # ensure consistent order
    text_files = [f for f in files if f.endswith(".txt")]
    first_files = text_files[:1]
    full_paths = [os.path.join(folder, f) for f in first_files]
    sampled_articles.extend(full_paths)

print(f"Selected {len(sampled_articles)} articles from {len(section_folders)} folders.")

merged_raw_text = ""

for file_path in sampled_articles:
    with open(file_path, "r", encoding="utf-8") as f:
        article_text = f.read().strip()
        article_text = re.sub(r"\n{2,}", "\n", article_text)
        merged_raw_text += article_text + "\n\n"  # double newlines between articles

# Save to a text file
with open("sampled_articles_merged_raw.txt", "w", encoding="utf-8") as f:
    f.write(merged_raw_text.strip())

print("✅ Saved merged original articles to 'sampled_articles_merged_raw.txt'")


#%% Getting word counts
text_path = "C:/Users/Ilsu/Desktop/School/Thesis/Project/corpora/bbc/merged-by-section/merged_articles_politics.txt"
with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()

print(len(text.split()))


