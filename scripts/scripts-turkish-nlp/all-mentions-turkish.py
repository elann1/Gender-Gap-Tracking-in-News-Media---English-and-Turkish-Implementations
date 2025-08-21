import pandas as pd
import spacy, spacy_transformers
import requests
import time
from collections import Counter
nlp = spacy.load("tr_core_news_lg")
API_KEY = ""

def get_all_names(text_path):
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()
    text_for_ner = nlp(text.strip())
    df = pd.DataFrame([(ent.text, ent.label_) for ent in text_for_ner.ents], columns=["Text", "Entity Label"])
    df_names = df[df["Entity Label"] == "PERSON"]
    names_list =  df_names["Text"].tolist()
    nominative_names_list = []
    for name in names_list:
        nominative = name.split("'")[0].split("’")[0]
        nominative_names_list.append(nominative)
    return(nominative_names_list)


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


def save_excel(df, section):
    gender_counts = df['gender'].value_counts()
    gender_percentages = df['gender'].value_counts(normalize=True) * 100

    df_summary = pd.DataFrame({
        'gender': gender_counts.index,
        'count': gender_counts.values,
        'percentage': gender_percentages.values
    })

    # Save to Excel
    filename = f"all-mentions-turkish-{section}.xlsx"
    df.to_excel(filename, index=False, engine='openpyxl')

    # Print stats
    print(f"Saved: {filename}")
    print("Number of names found:", len(df))
    print("Gender stats:")
    print(df_summary)

TEXT_PATH = ""
names_list = get_all_names(TEXT_PATH)
all_mentions_df = get_gender_data(names_list, API_KEY)
save_excel(all_mentions_df, "tech")

