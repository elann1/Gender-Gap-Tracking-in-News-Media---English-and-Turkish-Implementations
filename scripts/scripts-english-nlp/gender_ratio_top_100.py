#%%
import spacy
import pandas as pd
import time
from collections import Counter, defaultdict
import requests

#%%
API_KEY = "6852cfd827f9d5de88a7676a"
#TEXT_PATH = "C:/Users/Ilsu/Desktop/School/Thesis/Project/merged_articles_tech.txt"
nlp = spacy.load("en_core_web_sm")

#with open(TEXT_PATH, "r", encoding="utf-8") as f:
        #text = f.read()



#%%

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

def expand_partial_names(name_list):
    updated_names = []

    for i, name in enumerate(name_list):
        replacement = name
        for other in name_list:
            if name != other and name in other:
                # Check name is NOT the first word of the other
                if not other.startswith(name):
                    replacement = other
                    break
        updated_names.append(replacement) 

    return updated_names

#%%
file_path = "C:/Users/Ilsu/Desktop/School/Thesis/Project/stats/english-stats/all-mentions/all-mentions-names-gender-tech.xlsx"

# Load Excel file into a DataFrame
df = pd.read_excel(file_path)

names_list = df["name"].dropna().astype(str).tolist()
full_names_list = expand_partial_names(names_list)
full_name_counts = Counter(full_names_list)
sorted_names = full_name_counts.most_common()
df_counts = pd.DataFrame(sorted_names, columns=['name', 'count'])
first_hundred = list(df_counts['name'][:100])

df_gender_first_hundred = get_gender_data(first_hundred, API_KEY)


df_combined = pd.merge(df_gender_first_hundred, df_counts, on='name', how='left')
df_combined = df_combined[['name', 'count', 'gender', 'probability']]

gender_counts = df_gender_first_hundred['gender'].value_counts()
gender_percentages = df_gender_first_hundred['gender'].value_counts(normalize=True) * 100
df_summary_first_hundred = pd.DataFrame({
    'gender': gender_counts.index,
    'count': gender_counts.values,
    'percentage': gender_percentages.values
})

df_combined.to_excel("top_100_gender_stats-tech.xlsx", index=False)
print("The gender ratio of top 100 popular people:")
print(df_summary_first_hundred)

#%%