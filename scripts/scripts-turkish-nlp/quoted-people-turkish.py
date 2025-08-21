import spacy
import pandas as pd
from collections import Counter
import time
import requests

quote_verbs_dir_adv = ["söyledi", "söylerken",  "dedi", "derken", "paylaştı", "paylaşırken", "özetledi", "özetlerken", "anlattı", "anlatırken", "belirtti", "belirtirken",
                "ekledi", "eklerken", "açıkladı", "açıklarken", "bildirdi", "bildirirken", "vurguladı", "vurgularken", "duyurdu", "duyururken", "aktardı", 
                "aktarırken", "yazdı", "yazarken", "yansıttı", "yansıtırken", "savundu", "savunurken", "yalanladı", "yalanlarken", "cevapladı", "cevaplarken",
                "yanıtladı", "yanıtlarken", "sordu", "sorarken", "tekrarladı", "tekrarlarken", "iletti", "iletirken", "yayımladı", "yayımlarken", "konuştu",
                "konuşurken", "seslendi", "seslenirken"]
quote_verbs_adj = ["söyleyen", "diyen", "paylaşan", "özetleyen", "anlatan", "belirten", "ekleyen", "açıklayan", "bildiren", "vurgulayan", "duyuran", "aktaran",
                   "yazan", "yansıtan", "savunan", "yalanlayan", "cevaplayan", "yanıtlayan", "soran", "tekrarlayan", "ileten", "yayımlayan", "konuşan", "seslenen"]


API_KEY = ""

nlp = spacy.load("tr_core_news_lg")
def extract_quoted_names(text_path, quote_verbs_dir_adv, quote_verbs_adj):
    with open(text_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    articles = full_text.strip().split("\n\n")
    all_speakers = []

    for article in articles:
        parsed_text = nlp(article.strip())
        speakers = set()
    
        for ent in parsed_text.ents:
            if ent.label_ == "PERSON":
                for token in ent:
                    if token.dep_ in {"nsubj", "agent"} and token.head.text in quote_verbs_dir_adv:
                        speakers.add(ent.text)
                    for child in token.children:
                        if child.text in quote_verbs_adj:
                            speakers.add(ent.text)
                for token in parsed_text:
                    if token.text in quote_verbs_dir_adv:
                        for child in token.children:
                            if child.dep_ == "punct" and ent.start > child.i:
                                speakers.add(ent.text)
                                break  # avoid duplicates for the same match
        all_speakers.extend(speakers)
    return(all_speakers)

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
    filename = f"quotes-turkish-{section}.xlsx"
    df.to_excel(filename, index=False, engine='openpyxl')

    # Print stats
    print(f"Saved: {filename}")
    print("Number of names found:", len(df))
    print("Gender stats:")
    print(df_summary)


text_path = ""
names_list = extract_quoted_names(text_path, quote_verbs_dir_adv, quote_verbs_adj)
gendered_df = get_gender_data(names_list, API_KEY)
save_excel(gendered_df, "tech")
