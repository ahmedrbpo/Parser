import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower()

def extract_keywords(text):
    doc = nlp(text)
    return [token.lemma_.lower() for token in doc if token.pos_ in ['NOUN', 'PROPN', 'VERB', 'ADJ']]

def get_weighted_keywords(text):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])
    scores = dict(zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0]))
    return scores

def compare_keywords(resume_text, jd_text):
    resume_clean = clean_text(resume_text)
    jd_clean = clean_text(jd_text)

    resume_keywords = extract_keywords(resume_clean)
    jd_weights = get_weighted_keywords(jd_clean)

    matched = {kw: jd_weights[kw] for kw in resume_keywords if kw in jd_weights}
    unmatched = {kw: jd_weights[kw] for kw in jd_weights if kw not in resume_keywords}
    total_weight = sum(jd_weights.values())
    matched_weight = sum(matched.values())
    score = round((matched_weight / total_weight) * 100, 2) if total_weight else 0

    return {
        "matched_keywords": matched,
        "unmatched_keywords": unmatched,
        "match_score": score
    }