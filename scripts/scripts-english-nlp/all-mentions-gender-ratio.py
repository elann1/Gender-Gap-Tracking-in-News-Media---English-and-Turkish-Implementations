#%%
import pandas as pd
import spacy
import requests
import time
from collections import Counter
import openpyxl

#%%
API_KEY = ""
TEXT_PATH = ""
nlp = spacy.load("en_core_web_sm")

#%%
def get_all_names(text_path):
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()
    text_for_ner = nlp(text.strip())
    df = pd.DataFrame([(ent.text, ent.label_) for ent in text_for_ner.ents], columns=["Text", "Entity Label"])
    df_names = df[df["Entity Label"] == "PERSON"]
    return df_names["Text"].tolist()

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

names_list = get_all_names(TEXT_PATH)
df_gender = get_gender_data(names_list, API_KEY)
gender_counts = df_gender['gender'].value_counts()
gender_percentages = df_gender['gender'].value_counts(normalize=True) * 100
df_summary_all_mentions = pd.DataFrame({
    'gender': gender_counts.index,
    'count': gender_counts.values,
    'percentage': gender_percentages.values
})

df_gender.to_excel("all-mentions-names-gender-politics.xlsx", index=False)
df_summary_all_mentions.to_excel("all_mentions_politics_summary.xlsx", index=False)
print("Number of names found:")
print(len(names_list))
print("Gender stats:")
print(df_summary_all_mentions)


