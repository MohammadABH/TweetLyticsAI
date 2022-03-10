import axios from "axios";

export default async function fetchTweetWidgetApi(tweetId: number) {
  const response = await axios.get<any>(
    `https://publish.twitter.com/oembed?url=https://twitter.com/twitter/status/${tweetId}`
  );
  const data = response;
  return data;
}
