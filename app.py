import streamlit as st
import matplotlib.pyplot as plt
from parser import compare_keywords
from utils import load_pdf

st.set_page_config(page_title="Resume vs JD Analyzer", layout="centered")

st.title("📄 Resume Parser & JD Matcher")
st.write("Upload your resume and job description (PDF) to analyze keyword match and score.")

col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("Upload Resume (.pdf)", type=["pdf"])
with col2:
    jd_file = st.file_uploader("Upload Job Description (.pdf)", type=["pdf"])

if resume_file and jd_file:
    resume_text = load_pdf(resume_file)
    jd_text = load_pdf(jd_file)

    result = compare_keywords(resume_text, jd_text)

    st.subheader("✅ Matching Keywords (Weighted)")
    st.write({k: round(v, 3) for k, v in result["matched_keywords"].items()})

    st.subheader("❌ Unmatched Keywords from JD (Weighted)")
    st.write({k: round(v, 3) for k, v in result["unmatched_keywords"].items()})

    st.subheader("📊 Match Score")
    st.metric(label="Resume Match with JD", value=f"{result['match_score']}%")

    # Pie Chart
    labels = ['Matched', 'Unmatched']
    sizes = [sum(result["matched_keywords"].values()), sum(result["unmatched_keywords"].values())]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    # Bar Chart
    st.subheader("📈 Top JD Keywords by Weight")
    top_keywords = dict(sorted(result["unmatched_keywords"].items(), key=lambda x: x[1], reverse=True)[:10])
    fig2, ax2 = plt.subplots()
    ax2.bar(top_keywords.keys(), top_keywords.values(), color='orange')
    plt.xticks(rotation=45)
    st.pyplot(fig2)