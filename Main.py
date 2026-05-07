import time
import pandas as pd
from textblob import Textblob
from colorama import init,Fore
import random
# Initialize Colorama
init(autoreset=True)
#load the dataset
try:
    df=pd.read_csv("imdb_top_1000.csv")
except FileNotFoundError:
    print(Fore.RED+"File not found")
    raise SystemExit
# Extract all the genres
genres=sorted({
    g.strip() for xs in df['Genre'].dropna().str.split(", ")
    for g in xs
})
# Loading Animation
def dots():
    for _ in range(3):
        print(Fore.YELLOW+".",end="",flush=True)
        time.sleep(0.4)
# Sentiment Analysis
def senti(p):
    if p>0.1:
        return "positive 😊"
    elif p>-0.1:
        return "negative 😒"
    return "neutral 😐"
# Recommendation System
def recommend(genre=None,mood=None,rating=None,n=5):
    # Copy the dataset
    d=df.copy()
    if genre:
        d=d[d['Genre'].str.contains(genre,case=False, na=False)]
    if rating is not None:
        d=d[d["IMDB_Rating"]>=rating]
    if d.empty:
        return "No movies found"
    