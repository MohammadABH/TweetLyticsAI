import axios from "axios";

export default async function fetchTweetsApi(tweetId: number) {
  const response = await axios.get<TweetTreeAPIResponse>(
    `http://localhost:8000/api/analyze/${tweetId}`
  );
  const { data: tweetsResponse } = response;
  return tweetsResponse;
}
