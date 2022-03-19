import axios from "axios";
import mockData from "../mock_data/1500398661221576705.json";

export default async function fetchTweetsApi(tweetId: string) {
  const response = await axios.get<TweetTreeAPIResponse>(
    `http://localhost:8000/api/analyze/${tweetId}`
  );
  const { data: tweetsResponse } = response;
  return tweetsResponse;
}

// const timeout = (ms: number) => {
//   return new Promise((resolve) => setTimeout(resolve, ms));
// };

// export default async function fetchTweetsApi(tweetId: string) {
//   await timeout(100);
//   const tweetMockData: any = mockData;
//   return tweetMockData;
// }
