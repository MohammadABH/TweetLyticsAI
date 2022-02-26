from fastapi import FastAPI

from backend.services.tweet_tree_builder_service import TweetTreeBuilder

app = FastAPI()

@app.get("/api/health")
async def health_check():
    return {"message": "API is up and running!"}

@app.get("/api/analyze")
async def tweet_analyzer():
    tweet_tree = TweetTreeBuilder(1496855592027275273).get_tweet_tree()
    data = tweet_tree.get_json()

    return {"message": data}