import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import TweetTree from "../components/TweetTree";
import fetchTweetsApi from "../api/FetchTweets";

const TweetAnalysisPage = () => {
  const { id: tweetId } = useParams();
  const [tweets, setTweets] = useState<TweetTree | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  const fetchTweets = async () => {
    if (tweetId === undefined) setErrorMessage("Invalid Tweet URL ID");
    else {
      try {
        const parsedTweetId = parseInt(tweetId);
        const { response: tweetsResponse } = await fetchTweetsApi(
          parsedTweetId
        );
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
    <TweetTree tweetId={tweetId} tweets={tweets} errorMessage={errorMessage} />
  );
};

export default TweetAnalysisPage;
