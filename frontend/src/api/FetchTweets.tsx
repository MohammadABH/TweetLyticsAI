import axios from "axios";

import example1 from "../mock_data/example1.json";
import example2 from "../mock_data/example2.json";
import example3 from "../mock_data/example3.json";

const timeout = (ms: number) => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

export async function fetchCachedTweets(tweetExample: string) {
  await timeout(10);
  if (tweetExample === "tweetExample1") return example1;
  else if (tweetExample === "tweetExample2") return example2;
  else return example3;
}

export async function fetchTweetsApi(tweetId: string) {
  const response = await axios.get<TweetTreeAPIResponse>(
    `http://127.0.0.1:80/api/analyze/${tweetId}`
  );
  const { data: tweetsResponse } = response;
  console.log(tweetsResponse);
  return tweetsResponse;
}
