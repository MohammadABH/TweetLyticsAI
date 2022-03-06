from fastapi import FastAPI

from backend.controllers.TweetAnalyzerController import TweetAnalyzerController

app = FastAPI()
controller = TweetAnalyzerController()


@app.get("/api/health")
async def health_check():
    return {"message": "API is up and running!"}


@app.get("/api/analyze/{tweet_id}")
def tweet_analyzer(tweet_id: int):
    response = controller.analyze_tweet(tweet_id)

    return {"response": response}

