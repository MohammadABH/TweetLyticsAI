from fastapi import FastAPI

from backend.services.tweet_tree_builder_service import TweetTreeBuilder

app = FastAPI()

@app.get("/api/health")
async def health_check():
    return {"message": "API is up and running!"}

@app.get("/api/analyze/{tweet_id}")
def test_tweet_analyzer(tweet_id: int):
    tweet_tree = TweetTreeBuilder(tweet_id).get_tweet_tree()
    data = tweet_tree.get_json()

    return {"message": data}

@app.get("/api/test/analyze")
def test_tweet_analyzer():
    tweet_tree = TweetTreeBuilder(1496855592027275273).get_tweet_tree()
    data = tweet_tree.get_json()

    return {"message": data}
