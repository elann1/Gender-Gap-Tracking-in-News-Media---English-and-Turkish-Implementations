import pandas as pd

## MERGE DFS WITH ALL MENTIONS ##

excel_business = "C:/Users/Ilsu/Desktop/School/Thesis/Project/stats/english-stats/all-mentions/all-mentions-english-business.xlsx"
excel_entertainment = "C:/Users/Ilsu/Desktop/School/Thesis/Project/stats/english-stats/all-mentions/all-mentions-english-entertainment.xlsx"
excel_politics = "C:/Users/Ilsu/Desktop/School/Thesis/Project/stats/english-stats/all-mentions/all-mentions-english-politics.xlsx"
excel_sport = "C:/Users/Ilsu/Desktop/School/Thesis/Project/stats/english-stats/all-mentions/all-mentions-english-sport.xlsx"
excel_tech = "C:/Users/Ilsu/Desktop/School/Thesis/Project/stats/english-stats/all-mentions/all-mentions-english-tech.xlsx"

df_business = pd.read_excel(excel_business)
df_entertainment = pd.read_excel(excel_entertainment)
df_politics = pd.read_excel(excel_politics)
df_sport = pd.read_excel(excel_sport)
df_tech = pd.read_excel(excel_tech)

bbc_all_mentions = pd.concat([df_business, df_entertainment, df_politics, df_sport, df_tech], ignore_index=True)

#%%
## TOP 100 STATS ##
def top_repeated_names(df, top_n=150):
    # Count how many times each name appears
    name_counts = df['name'].value_counts().reset_index()
    name_counts.columns = ['name', 'mention count']

    # Merge back to original DataFrame to get gender and probability
    df_unique = df.drop_duplicates(subset='name', keep='first')[['name', 'gender', 'probability']]

    # Merge counts with metadata
    result = pd.merge(name_counts, df_unique, on='name', how='left')

    # Take the top N most repeated names
    return result.head(top_n)
top_150_bbc = top_repeated_names(bbc_all_mentions)
top_150_bbc.to_excel("top_150_bbc.xlsx", index=False, engine='openpyxl')
#%%
def top_10_by_gender(df):
    # First, drop rows where gender is not male or female
    filtered = df[df['gender'].isin(['male', 'female'])]

    # Count mentions per name
    name_counts = filtered['name'].value_counts().reset_index()
    name_counts.columns = ['name', 'mention count']

    # Keep gender info from the first occurrence
    df_unique = filtered.drop_duplicates(subset='name', keep='first')[['name', 'gender', 'probability']]

    # Merge counts with gender/probability
    result = pd.merge(name_counts, df_unique, on='name', how='left')

    # Separate top 10 for each gender
    top_women = result[result['gender'] == 'female'].head(14)
    top_men = result[result['gender'] == 'male'].head(14)

    # Combine into one DataFrame
    top_combined = pd.concat([top_women, top_men], ignore_index=True)
    return top_combined
#%%
top_10_by_gender_bbc = top_10_by_gender(bbc_all_mentions)
top_10_by_gender_bbc.to_excel("top_10_by_gender_bbc.xlsx", index=False, engine='openpyxl')
#%%
## TURKISH ##
excel_culture_tr = "C:/Users/Ilsu/Desktop/School/Thesis/Project/stats/turkish-stats/all-mentions/all-mentions-turkish-clean-culture.xlsx"
excel_economy_tr = "C:/Users/Ilsu/Desktop/School/Thesis/Project/stats/turkish-stats/all-mentions/all-mentions-turkish-clean-economy.xlsx"
excel_politics_tr = "C:/Users/Ilsu/Desktop/School/Thesis/Project/stats/turkish-stats/all-mentions/all-mentions-turkish-clean-politics.xlsx"
excel_sport_tr = "C:/Users/Ilsu/Desktop/School/Thesis/Project/stats/turkish-stats/all-mentions/all-mentions-turkish-clean-sport.xlsx"
excel_tech_tr = "C:/Users/Ilsu/Desktop/School/Thesis/Project/stats/turkish-stats/all-mentions/all-mentions-turkish-clean-tech.xlsx"

df_culture_tr = pd.read_excel(excel_culture_tr)
df_economy_tr = pd.read_excel(excel_culture_tr)
df_politics_tr = pd.read_excel(excel_politics_tr)
df_sport_tr = pd.read_excel(excel_sport_tr)
df_tech_tr = pd.read_excel(excel_tech_tr)
milliyet_all_mentions = pd.concat([df_culture_tr, df_economy_tr, df_politics_tr, df_sport_tr, df_tech_tr], ignore_index=True)
top_150_milliyet = top_repeated_names(milliyet_all_mentions)
top_150_milliyet.to_excel("top_150_milliyet.xlsx", index=False, engine='openpyxl')
top_10_by_gender_milliyet = top_10_by_gender(milliyet_all_mentions)
top_10_by_gender_milliyet.to_excel("top_10_by_gender_milliyet.xlsx", index=False, engine='openpyxl')
# %%
top_10_by_gender_milliyet = top_10_by_gender(milliyet_all_mentions)
top_10_by_gender_milliyet.to_excel("top_10_by_gender_milliyet.xlsx", index=False, engine='openpyxl')
# %%
