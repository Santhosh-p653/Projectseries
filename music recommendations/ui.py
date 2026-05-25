import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Page Config
st.set_page_config(
    page_title="AI Music Recommender",
    page_icon="🎧",
    layout="wide"
)


# Custom CSS
st.markdown(
    """
    <style>
    .main {
        background-color: #0f172a;
    }

    h1 {
        color: white;
        text-align: center;
        font-size: 50px;
    }

    .stSelectbox label {
        color: white !important;
        font-size: 20px;
    }

    .song-card {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
        color: white;
        font-size: 20px;
        box-shadow: 0px 0px 10px rgba(255,255,255,0.1);
    }

    .subtitle {
        color: #cbd5e1;
        text-align: center;
        font-size: 20px;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Title
st.markdown("<h1>🎧 AI Music Recommendation System</h1>", unsafe_allow_html=True)

st.markdown(
    "<p class='subtitle'>Find songs similar to your favorite tracks using Machine Learning</p>",
    unsafe_allow_html=True
)


# Load Dataset
songs = pd.read_csv("songs.csv")


# Combine Features
songs["features"] = (
    songs["genre"] + " " +
    songs["mood"] + " " +
    songs["artist"]
)


# TF-IDF
tfidf = TfidfVectorizer()

tfidf_matrix = tfidf.fit_transform(songs["features"])


# Cosine Similarity
similarity = cosine_similarity(tfidf_matrix)


# Recommendation Function
def recommend(song_name):

    matches = songs[songs["title"] == song_name]

    if matches.empty:
        return []

    index = matches.index[0]

    scores = list(enumerate(similarity[index]))

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    scores = scores[1:6]

    recommended = []

    for item in scores:
        recommended.append(
            songs.iloc[item[0]]["title"]
        )

    return recommended


# Center Layout
col1, col2, col3 = st.columns([1,2,1])

with col2:

    song_name = st.selectbox(
        "Choose Your Song",
        songs["title"].values
    )

    if st.button("🎵 Recommend Songs", use_container_width=True):

        recommendations = recommend(song_name)

        st.write("")
        st.subheader("✨ Recommended For You")

        for song in recommendations:

            st.markdown(
                f"<div class='song-card'>🎶 {song}</div>",
                unsafe_allow_html=True
            )


# Footer
st.write("")
st.caption("Powered by TF-IDF + Cosine Similarity")
