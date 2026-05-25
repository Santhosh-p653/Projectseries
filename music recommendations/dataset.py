import pandas as pd
import random

titles = [
    "Moonlight Echo",
    "Neon Dreams",
    "Silent Waves",
    "Dark Paradise",
    "Golden Sky",
    "Electric Soul",
    "Crystal Rain",
    "Velvet Night",
    "Burning Stars",
    "Ocean Heart"
]

genres = [
    "Pop",
    "Rock",
    "HipHop",
    "LoFi",
    "Jazz",
    "EDM",
    "Classical",
    "Romantic",
    "Indie",
    "KPop"
]

moods = [
    "Happy",
    "Sad",
    "Energetic",
    "Calm",
    "Romantic",
    "Dark",
    "Dreamy"
]

artists = [
    "Ariana",
    "Drake",
    "BTS",
    "Taylor",
    "Weeknd",
    "ImagineDragons",
    "DuaLipa",
    "Billie",
    "Shawn",
    "Olivia"
]

songs = []

for i in range(100):

    title = random.choice(titles) + " " + str(i)

    genre = random.choice(genres)

    mood = random.choice(moods)

    artist = random.choice(artists)

    songs.append([
        title,
        genre,
        mood,
        artist
    ])

df = pd.DataFrame(
    songs,
    columns=["title", "genre", "mood", "artist"]
)

df.to_csv("songs.csv", index=False)

print("songs.csv created successfully!")                      