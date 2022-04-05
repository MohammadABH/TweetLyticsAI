import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import TweetTree from "../components/TweetTree";
import { fetchTweetsApi, fetchCachedTweets } from "../api/FetchTweets";

const TweetAnalysisPage = () => {
  const { id: tweetIdParam } = useParams();
  const [tweetId, setTweetId] = useState<string | undefined>(tweetIdParam);
  const [tweets, setTweets] = useState<TweetTree | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  const fetchTweets = async () => {
    if (tweetId === undefined) setErrorMessage("Invalid Tweet URL ID");
    else if (tweetId.startsWith("tweetExample")) {
      const { response: tweetsResponse } = await fetchCachedTweets(tweetId);
      setTweets(tweetsResponse as TweetTree);
      setErrorMessage("");
      setTweetId(tweetsResponse.tweet_tree.name);
    } else {
      try {
        const { response: tweetsResponse } = await fetchTweetsApi(tweetId);
        setTweets(tweetsResponse);
        setErrorMessage("");
      } catch (error) {
        setErrorMessage(
          "Something went wrong while processing your request, make sure the Tweet URL is valid and try again!"
        );
      }
    }
  };

  useEffect(() => {
    fetchTweets();
  }, []);
  return (
    <TweetTree
      tweetId={tweetId}
      tweets={tweets}
      errorMessage={errorMessage}
      data-testid="tweet-tree"
    />
  );
};

export default TweetAnalysisPage;
