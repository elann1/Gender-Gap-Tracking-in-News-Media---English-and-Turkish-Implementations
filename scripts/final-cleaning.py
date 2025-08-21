import pandas as pd

#%%
excel_path = "C:/Users/Ilsu/Desktop/School/Thesis/Project/stats/english-stats/quoted/old/quoted-names-gender-tech.xlsx"
df = pd.read_excel(excel_path)

## DELETE ROWS WITH NO NAMES ##
df = df[df['name'].notna() & (df['name'].str.strip() != '')]
df_updated = df.copy()

## MATCH LAST NAME MENTIONS TO FULL NAME MENTIONS ##
for idx, row in df_updated.iterrows():
    name = row['name']
    if ' ' not in name:
        match = df_updated[df_updated['name'].astype(str).str.endswith(' ' + name, na=False)]
        if not match.empty:
            df_updated.loc[idx] = match.iloc[0]



## IGNORE PROBABILITIES LOWER THAN 80% ##
df_updated['probability'] = pd.to_numeric(df_updated['probability'], errors='coerce')
df_updated.loc[df_updated['probability'] < 80, 'gender'] = 'null'


## MATCH GENDER TO GENDERED TITLES ##

# Ensure all name values are strings (in case there are NaNs)
df_updated['name'] = df_updated['name'].astype(str)

# Define title-based gender rules
# English titles
df_updated.loc[df_updated['name'].str.contains(r'\b(?:Ms|Mrs|Miss)\b', case=False, na=False), 'gender'] = 'female'
df_updated.loc[df_updated['name'].str.contains(r'\bMr\b', case=False, na=False), 'gender'] = 'male'

# Turkish titles
df_updated.loc[df_updated['name'].str.contains(r'\b(?:Bayan|Hanım)\b', case=False, na=False), 'gender'] = 'female'
df_updated.loc[df_updated['name'].str.contains(r'\b(?:Bey|Bay)\b', case=False, na=False), 'gender'] = 'male'

## SAVE TONEW EXCEL ##
filename = f"quoted-clean-english-tech.xlsx"
df_updated.to_excel(filename, index=False, engine='openpyxl')


## ALL MENTIONS AND QUOTES STATS ##
full_stats = df_updated['gender'].value_counts(dropna=False).rename_axis('gender').reset_index(name='count')
full_stats['percentage'] = (full_stats['count'] / len(df_updated) * 100).round(2)
non_null_df = df_updated[df_updated['gender'].isin(['male', 'female'])]

non_null_stats = non_null_df['gender'].value_counts().rename_axis('gender').reset_index(name='count')
non_null_stats['percentage'] = (non_null_stats['count'] / len(non_null_df) * 100).round(2)
female_count = (df_updated['gender'] == 'female').sum()
male_count = (df_updated['gender'] == 'male').sum()
female_to_male_ratio = f"{female_count}:{male_count}"

output_path = "gender_statistics.csv"


# 1. Save full_stats
with open(output_path, "w", encoding="utf-8") as f:
    f.write("Full Gender Stats (All)\n")
    full_stats.to_csv(f, index=False)
    f.write("\n")

    # 2. Save non_null_stats
    f.write("Non-Null Gender Stats (Only Male/Female)\n")
    non_null_stats.to_csv(f, index=False)
    f.write("\n")

    # 3. Save female-to-male ratio
    f.write("Female to Male Ratio\n")
    f.write(f"{female_to_male_ratio}\n")




# %%
