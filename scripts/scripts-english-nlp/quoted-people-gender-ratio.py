import spacy
import pandas as pd
import requests
import time
from collections import Counter

text_path = ""
API_KEY=""
quote_verbs = [
        "acknowledged", "added", "addressed", "admitted", "announced", "argued",
        "believed", "claimed", "concluded", "confirmed", "continued", "declared",
        "described", "ensured", "estimated", "explained", "found", "indicated",
        "informed", "insisted", "noted", "pointed", "predicted", "provided",
        "released", "replied", "reported", "responded", "said", "stated", "suggested",
        "told", "testified", "thought", "tweeted", "warned", "wrote", "acknowledges", "adds", "addresses", "admitts", "announces", "argues",
        "believes", "claims", "concludes", "confirms", "continues" "describes", "ensures", "estimates", "explains", "finds", "indicates",
        "informs", "insists", "notes", "points", "predicts", "provides",
        "releases", "replies", "reports", "responds", "says", "states", "suggests",
        "tells", "declares", "testifies", "thinks", "tweets", "warns", "writes"
    ]
nlp = spacy.load("en_core_web_sm")

def extract_quoted_names(text_path, quote_verbs):
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()
    parsed_text = nlp(text.strip())
    speakers: list[str] = []
    for token in parsed_text:
        if token.pos_ == "VERB" and token.text in quote_verbs:
            for child in token.children:
                if child.dep_ in {"nsubj", "agent"} and child.ent_type_ == "PERSON":
                    speakers.append(child.text)
            
            for child in token.children:
                if child.dep_ == "punct":
                    next_tokens = [t for t in child.subtree if t.i > child.i]
                    for nt in next_tokens:
                        if nt.ent_type_ == "PERSON":
                            speakers.append(nt.text)
    
    #Get full names from surnames for gender recognition
    matches = []
    for ent in parsed_text.ents:
        if ent.label_ == "PERSON":
            name_parts = ent.text.split()
            if name_parts and name_parts[-1] in speakers:
                matches.append(ent.text)
    return matches

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

speakers = extract_quoted_names(text_path, quote_verbs)
df_gender = get_gender_data(speakers, API_KEY)
gender_counts = df_gender['gender'].value_counts()
gender_percentages = df_gender['gender'].value_counts(normalize=True) * 100
df_summary_quoted_names = pd.DataFrame({
    'gender': gender_counts.index,
    'count': gender_counts.values,
    'percentage': gender_percentages.values
})

df_gender.to_excel("quoted-names-gender-tech.xlsx", index=False)
df_summary_quoted_names.to_excel("all_mentions_tech_summary.xlsx", index=False)
print("Number of quoted people found:")
print(len(speakers))
print("Gender stats:")
print(df_summary_quoted_names)

