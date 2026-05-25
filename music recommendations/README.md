Music Recommendation System is a content-based filtering project that suggests similar songs based on their textual features.
It uses TF-IDF Vectorizer to convert song metadata or lyrics into numerical vectors.
These vectors capture the importance of words in each song.
Cosine similarity is then applied to measure how close two songs are in vector space.
When a user selects a song, the system finds songs with the highest similarity scores.
The top matching songs are returned as recommendations.
Streamlit is used to build an interactive web interface for easy user interaction.
The system is lightweight and does not require user history or login data.
It works purely on song content, making it simple and efficient.
Overall, it demonstrates NLP and recommendation system fundamentals in a practical way.