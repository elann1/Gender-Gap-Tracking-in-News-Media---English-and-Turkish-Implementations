import spacy
import pandas as pd
import time
from collections import Counter
import requests

API_KEY = ""
TEXT_PATH = ""
nlp = spacy.load("en_core_web_sm")

with open(TEXT_PATH, "r", encoding="utf-8") as f:
        text = f.read()

def get_gender_data(names_list, api_key, batch_size=100, pause=1):
    name_counts = Counter(names_list)
    unique_names = list(name_counts.keys())
    all_results = []

    for i in range(0, len(unique_names), batch_size):
        batch = unique_names[i:i + batch_size]
        name_fields = '&'.join([f'name[]={name}' for name in batch])
        payload = f"{name_fields}&key={api_key}"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        url = "https://api.genderapi.io/api/"

        try:
            
            response = requests.request("POST", "https://api.genderapi.io/api/", headers=headers, data=payload)
            response.raise_for_status()
            data = response.json().get("names", [])
            all_results.extend(data)
        except Exception as e:
            print(f"Error during API request (batch {i//batch_size + 1}): {e}")

        time.sleep(pause)

    expanded_results = []
    for entry in all_results:
        name = entry.get("q")
        gender = entry.get("gender")
        probability = entry.get("probability")
        count = name_counts.get(name, 0)
        for _ in range(count):
            expanded_results.append({
                "name": name,
                "gender": gender,
                "probability": probability
            })

    return pd.DataFrame(expanded_results)

articles = [a.strip() for a in text.split("\n\n") if a.strip()]

article_data = []  # to store data for each article

for i, article in enumerate(articles, start=1):
    doc = nlp(article)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    if not names:
        article_data.append({
            "Article Number": i,
            "Male Count": 0,
            "Female Count": 0,
            "Gender Tag": "Unknown"
        })
        continue

    df_gender = get_gender_data(names, API_KEY)
    gender_counts = df_gender["gender"].value_counts()

    male_count = gender_counts.get("male", 0)
    female_count = gender_counts.get("female", 0)

    if male_count > female_count:
        tag = "Male"
    elif female_count > male_count:
        tag = "Female"
    else:
        tag = "Unknown"

    article_data.append({
        "Article Number": i,
        "Male Count": male_count,
        "Female Count": female_count,
        "Gender Tag": tag
    })

# Create DataFrame
df_article_stats = pd.DataFrame(article_data)

# Save to Excel
df_article_stats.to_excel("article-gender-tags-tech.xlsx", index=False)

#Create summary DataFrame
df_summary_stats = (
    df_article_stats["Gender Tag"]
    .value_counts(normalize=False)
    .reset_index(name="Count")
    .rename(columns={"index": "Gender Tag"})
)

df_summary_stats["Percentage"] = (
    df_summary_stats["Count"] / df_summary_stats["Count"].sum()
) * 100

print("Per-article gender tagging saved to Excel.")
print(df_article_stats.head())
print("Summary statistics:")
print(df_summary_stats)

