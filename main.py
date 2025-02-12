import nltk
nltk.download('vader_lexicon')

from fastapi import FastAPI
import requests
from nltk.sentiment import SentimentIntensityAnalyzer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
sia = SentimentIntensityAnalyzer()

# Permettiamo le richieste dal frontend Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Qui puoi mettere l'URL di Next.js in produzione
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/jokes")
def get_jokes():
    api_url = "https://api.chucknorris.io/jokes/random"
    jokes = []

    for _ in range(10):
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Solleva un'eccezione se la risposta non è OK (status_code != 200)
            joke = response.json().get('value')
            if joke:
                sentiment = sia.polarity_scores(joke)['compound']
                sentiment_label = "Positivo" if sentiment > 0.05 else "Negativo" if sentiment < -0.05 else "Neutro"
                jokes.append({"text": joke, "sentiment": sentiment_label})
            else:
                return {"error": "Joke not found in response"}
        except requests.exceptions.RequestException as e:
            # Se c'è un errore nella richiesta, lo logghiamo
            return {"error": f"Errore API: {str(e)}"}

    return {"jokes": jokes}