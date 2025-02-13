import asyncio

import nltk
nltk.download('vader_lexicon')

from fastapi import FastAPI
import aiohttp
# import requests
from nltk.sentiment import SentimentIntensityAnalyzer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
sia = SentimentIntensityAnalyzer()

# Permettiamo le richieste dal frontend Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chuck-front.vercel.app/"],  # Qui puoi mettere l'URL di Next.js in produzione
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
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
"""

# Uso le funzioni asincrone come consigliato dal tutor

async def fetch_joke(session):
    api_url = "https://api.chucknorris.io/jokes/random"
    try:
        async with session.get(api_url) as response:
            response.raise_for_status()  # Solleva un errore se il codice di stato HTTP non è 2xx
            joke_data = await response.json()
            joke = joke_data.get("value")
            sentiment = sia.polarity_scores(joke)["compound"]
            sentiment_label = "Positivo" if sentiment > 0.05 else "Negativo" if sentiment < -0.05 else "Neutro"
            return {"text": joke, "sentiment": sentiment_label}
    except Exception as e:
        return {"error": str(e)}

@app.get("/jokes")
async def get_jokes():
    """
    aiohttp per fare chiamate API in modo asincrono

    asyncio.gather() per ottenere più battute in parallelo.
    """
    async with aiohttp.ClientSession() as session:
        jokes = await asyncio.gather(*(fetch_joke(session) for _ in range(10)))
    return {"jokes": jokes}