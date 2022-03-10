import React, { useEffect } from "react";
import { Tweet } from "react-twitter-widgets";
import fetchTweetWidgetApi from "../api/FetchTweetWidget";

interface IProps {
  tweetId: string;
}

const TweetWidget = ({ tweetId }: IProps) => {
  const fetchTweetWidget = async () => {
    const parsedTweetId = parseInt(tweetId);
    const res = fetchTweetWidgetApi(parsedTweetId);
    console.log(res);
  };

  useEffect(() => {
    fetchTweetWidget();
  }, []);
  return (
    <div></div>
    // <Tweet tweetId={tweetId} renderError={(_err) => "Could not load tweet! "} />
  );
};

export default TweetWidget;
