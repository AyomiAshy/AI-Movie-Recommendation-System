import time
import pandas as pd
from textblob import TextBlob
from colorama import init, Fore

init(autoreset=True)

# load dataset
try:
    df = pd.read_csv("imdb_top_1000.csv")
except FileNotFoundError:
    print(Fore.RED + "File not found")
    raise SystemExit

# extract genres
genres = sorted({
    g.strip() for xs in df['Genre'].dropna().str.split(", ")
    for g in xs
})

# loading animation
def dots():
    for _ in range(3):
        print(Fore.YELLOW + ".", end="", flush=True)
        time.sleep(0.4)

# sentiment
def senti(p):
    if p > 0.1:
        return "positive 😊"
    elif p < -0.1:   # FIXED
        return "negative 😒"
    return "neutral 😐"

# recommendation
def recommend(genre=None, mood=None, rating=None, n=5):
    d = df.copy()

    if genre:
        d = d[d['Genre'].str.contains(genre, case=False, na=False)]

    if rating is not None:
        d = d[d["IMDB_Rating"] >= rating]

    if d.empty:
        return "No movies found"

    mood_polarity = TextBlob(mood).sentiment.polarity if mood else 0
    results = []

    d = d.sample(frac=1).reset_index(drop=True)

    for _, row in d.iterrows():
        overview = row.get("Overview")

        if pd.isna(overview):
            continue

        movie_polarity = TextBlob(overview).sentiment.polarity

        if mood:   # FIXED
            if mood_polarity > 0 and movie_polarity < 0:
                continue
            if mood_polarity < 0 and movie_polarity > 0:
                continue

        results.append((row["Series_Title"], movie_polarity))

        if len(results) == n:
            break

    return results if results else "No recommendations were found"

# display
def show(recs, name):
    print(Fore.YELLOW + f"\nRecommendations for {name}:")
    for i, (title, polarity) in enumerate(recs, 1):
        print(f"{Fore.CYAN}{i}. {title} ({senti(polarity)})")

# get genre
def get_genre():
    print(Fore.GREEN + "Available Genres:")
    for i, g in enumerate(genres, 1):
        print(f"{Fore.CYAN}{i}. {g}")

    while True:
        choice = input(Fore.YELLOW + "\nEnter genre number or name: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(genres):
            return genres[int(choice) - 1]

        choice = choice.title()
        if choice in genres:
            return choice

        print(Fore.RED + "INVALID INPUT")   # FIXED

# get rating
def get_rating():
    while True:
        x = input(Fore.YELLOW + "Enter your rating: ").strip()

        try:
            r = float(x)
            if 0 <= r <= 10:   # FIXED
                return r
            else:
                print(Fore.RED + "Rating out of range")
        except:
            print(Fore.RED + "Invalid Input")

# main
name = input(Fore.MAGENTA + "What is your name: ").strip()
print(Fore.GREEN + f"Hey {name}! Let's find you a movie")

genre = get_genre()

mood = input(Fore.YELLOW + "\nHow are you feeling today?: ").strip()

print(Fore.BLUE + "Analyzing mood", end="")
dots()

mp = TextBlob(mood).sentiment.polarity
print(Fore.GREEN + f"\nDetected mood: {senti(mp)}")

rating = get_rating()

print(Fore.BLUE + "\nFinding movies", end="")
dots()

recs = recommend(genre, mood, rating)

if isinstance(recs, str):
    print(Fore.RED + recs)
else:
    show(recs, name)