import os

# Set the folder path and output file name
folder_path = "" 
output_path = "merged_articles_tech.txt"

# Get the first 380 .txt files (sorted for consistency)
all_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".txt")])[:380]

# Read and clean each article
articles = []
for filename in all_files:
    with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
        content = f.read().strip()
        cleaned = content.replace("\n\n", "\n").strip()
        if cleaned:  
            articles.append(cleaned)

# Join articles with double newlines
merged_text = "\n\n".join(articles)

# Save to file
with open(output_path, "w", encoding="utf-8") as f:
    f.write(merged_text)

print(f"Merged {len(articles)} articles into '{output_path}'")



#%% cell to clean "'s" occurences
# Set the file path
file_path = "C:/Users/Ilsu/Desktop/School/Thesis/Project/merged_articles_tech.txt"  

# Read the text
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace all occurrences of "'s"
cleaned_text = text.replace("'s", "")

# Save back to the same file (or change the path to create a new file)
with open(file_path, "w", encoding="utf-8") as f:
    f.write(cleaned_text)

print("All occurrences of `'s` have been removed.")


# %% cell to truncate the 2 sections: politics and tech to 1000000 characters for the NER limit
# Path to your .txt file
file_path = "C:/Users/Ilsu/Desktop/School/Thesis/Project/merged_articles_tech.txt"  

# Set the character limit
char_limit = 1_000_000

# Read the full text
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Keep only the first 1,000,000 characters
truncated_text = text[:char_limit]

# Overwrite the file with truncated content
with open(file_path, "w", encoding="utf-8") as f:
    f.write(truncated_text)

print(f"Truncated the file to {char_limit} characters.")

