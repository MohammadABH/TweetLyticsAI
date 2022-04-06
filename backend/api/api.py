from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.controllers.tweet_analyzer_controller import TweetAnalyzerController

# Create the API and handle CORS middleware config
app = FastAPI()
controller = TweetAnalyzerController()
origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/api/health", tags=["health"])
async def health_check() -> dict:
    """
    :return: healthy status endpoint
    """
    return {"response": "API is up and running!"}


@app.get("/api/analyze/{tweet_id}", tags=["analyze"])
def tweet_analyzer(tweet_id: int) -> dict:
    """
    :param tweet_id:    the tweet ID to compute the analysis on
    :return:            argumentation model and analysis of the input tweet
    """
    try:
        response = controller.analyze_tweet(tweet_id)

        return {"response": response}
    except:
        raise HTTPException(status_code=500,
                            detail="Oops! Something went wrong while processing your request. Make sure the Tweet ID "
                                   "passed is valid and try again later.")

