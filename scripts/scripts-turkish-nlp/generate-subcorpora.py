import os
import re
import pandas as pd
corpus_path = ""
corpus_df = pd.read_csv(corpus_path)
clean_corpus_df = corpus_df.drop_duplicates(subset='news')

# categories: 'Gündem' 'Ekonomi' 'Spor' 'Siyaset' 'Dünya' 'Yaşam' 'Pazar' 'Ege'
# 'Magazin' 'Kültür_Sanat' 'Teknoloji_Bilim' 'Cumartesi'

culture_df = clean_corpus_df[clean_corpus_df['category'] == 'Kültür_Sanat']
culture_subcorp = '\n\n'.join(culture_df['news'].astype(str).head(280))
with open('milliyet_culture.txt', 'w', encoding='utf-8') as f:
    f.write(culture_subcorp)


# Extract rows into new dataframes by section 
economy_df = clean_corpus_df[clean_corpus_df['category'] == 'Ekonomi']
sport_df = clean_corpus_df[clean_corpus_df['category'] == 'Spor']
politics_df = clean_corpus_df[clean_corpus_df['category'] == 'Siyaset']
culture_df = clean_corpus_df[clean_corpus_df['category'] == 'Kültür_Sanat']
tech_df = clean_corpus_df[clean_corpus_df['category'] == 'Teknoloji_Bilim']

# Create subcorpora by section
economy_subcorp = '\n\n'.join(economy_df['news'].astype(str).head(280))
sport_subcorp = '\n\n'.join(sport_df['news'].astype(str).head(280))
politics_subcorp = '\n\n'.join(politics_df['news'].astype(str).head(280))
culture_subcorp = '\n\n'.join(culture_df['news'].astype(str).head(280))
tech_subcorp = '\n\n'.join(tech_df['news'].astype(str).head(480))

# Save subcorpora as .txt files
with open('milliyet_tech.txt', 'w', encoding='utf-8') as f:
    f.write(tech_subcorp)

corpus_path = ""
# Read original file
with open(corpus_path, "r", encoding="utf-8") as f:
    text = f.read()

# Split into paragraphs
paragraphs = text.split("\n\n")

# Take the first 50
first_50 = paragraphs[:50]

# Join back into text
output_text = "\n\n".join(first_50)

# Save to new file
with open("sample_corpus.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

import re

# Load the text file
with open("corpus_path", "r", encoding="utf-8") as f:
    text = f.read()

# Split into paragraphs
paragraphs = text.split("\n\n")

# Process paragraphs
processed = []
for para in paragraphs:
    # Remove two leading words followed by "." or " - "
    new_para = re.sub(r"^\s*\b\w+\b\s+\b\w+\b\s*(?:\.| - )\s*", "", para)
    processed.append(new_para)

# Join and save the result
with open("culture-new.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(processed))

#
input_path = ""
output_path = input_path  # This will overwrite the original file

with open(input_path, "r", encoding="utf-8") as f:
    text = f.read()

# Keep the first 1,000,000 characters
cropped_text = text[:1_000_000]

with open(output_path, "w", encoding="utf-8") as f:
    f.write(cropped_text)

print("Cropped to first 1,000,000 characters and saved.")
