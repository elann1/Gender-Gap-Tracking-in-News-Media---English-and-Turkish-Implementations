# Gender Gap Tracking in News Media via NLP tools

## Master’s Dissertation Project — System Creation and English and Turkish Implementations

This repository contains the full implementation for my master’s dissertation *“Cross-Linguistic Gender Gap Tracking in Media Texts using NLP Tools: Implementation Cases of English and Turkish”*

The project applies Natural Language Processing (NLP) to large English (BBC) and Turkish (Milliyet) news corpora to analyze gender representation.
It focuses on the degree and the manner of representation of men and women in the news, using:

- Named Entity Recognition (NER) (spaCy)

- Dependency Parsing (speaker attribution)

- Gender Prediction API (GenderAPI.io)

- Statistical aggregation and Excel outputs

The English corpus is analyzed first to establish a methodology, which is then adapted for the Turkish corpus, highlighting cross-linguistic challenges.

---

## Repository Structure
### 1. English Corpus Analysis (BBC News)

Located in `scripts/english/`

- ### Data Preparation

  - `merge-section-articles.py` → merge and clean raw BBC articles

  - `text-sampling.py` → select representative sample articles

- ### Section-Based Gender Ratio Analysis

  - `all-mentions-gender-ratio.py` → extract all names and compute gender ratios

  - `article_gender_ratio.py` → assign gender tags per article

  - `quoted-people-gender-ratio.py` → identify quoted speakers and their gender balance

- ### Frequency-Based Statistics

  - `gender_ratio_top_100.py` → analyze top 100 most frequently mentioned names

  - `top-10-counts.py` → compute top 10 most mentioned men and women

### 2. Turkish Corpus Analysis (Milliyet News)

Located in `scripts/turkish/`

- ### Corpus Generation

  - `generate-subcorpora.py` → build section-based subcorpora (Politics, Economy, Sport, Culture, Tech)

- ### Section-Based Gender Ratio Analysis

  - `all-mentions-turkish.py` → extract all names, normalize inflected forms, and compute gender ratios

  - `article_gender_ratio_turkish.py` → assign gender tags per article

  - `quoted-people-turkish.py` → detect quoted speakers using Turkish-specific verb/adjective lists

- ### Frequency-Based Statistics

  - `gender_ratio_top_100_turkish.py` → analyze top 100 most frequently mentioned names


### 3. Final Cleaning and Statistics

Located in `scripts/final/`

- `final-cleaning.py` → clean extracted names, resolve surname-only mentions, filter low-probability predictions (<80%), and apply gendered titles (e.g., Mr., Ms., Bey, Hanım)

- `final-stats.py` → merge English and Turkish results into cross-linguistic comparative statistics

## Requirements

- Python 3.9+
- spaCy (+ models: `en_core_web_sm`, `tr_core_news_lg`)

- pandas

- requests

- openpyxl

Install dependencies:

`pip install spacy pandas requests openpyxl`

`python -m spacy download en_core_web_sm`

`python -m spacy download tr_core_news_lg`

## Usage

1. ### Prepare corpora:

  - Place English BBC `.txt` files in `corpora/bbc/` (by section).

  - Place Turkish Milliyet dataset (`filtrelenmis_derlem.csv`) in `corpora/milliyet/`.

  - Run `generate-subcorpora.py` to create section-level `.txt` files for Turkish.

2. ### Run English pipeline:

`python merge-section-articles.py`

`python all-mentions-gender-ratio.py`

`python quoted-people-gender-ratio.py`

`python gender_ratio_top_100.py`


3. ### Run Turkish pipeline:

`python generate-subcorpora.py`

`python all-mentions-turkish.py`

`python quoted-people-turkish.py`

`python gender_ratio_top_100_turkish.py`


4. ### Clean and aggregate results:

`python final-cleaning.py`

`python final-stats.py`


5. ### Outputs:
   Excel files containing gender ratios and summary statistics.

## Metrics Produced

- **All mentions ratio:** statistics of all women and men in the corpora.

- **Quoted speakers ratio:**  statistics of all quoted women and men in the corpora.

- **Article-level ratio:** distribution of women/men dominance across articles.

- **Top 100 stats:** women/men distribution of the 100 most mentioned people across the main corpus

- **Mentions of Top 10 Most Mentioned Men and Women**

The statistics from these metrics are then used to calculate Gender Gap Scores for each subcorpus and then the overall newspaper corpus.

## Research Impact

This project provides a computational framework for tracking gender representation in media texts across languages. By applying identical methodologies to English and Turkish corpora, it demonstrates both structural biases in media coverage and linguistic challenges in multilingual NLP.
