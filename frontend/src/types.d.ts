type TweetSentiment = "positive" | "neutral" | "negative";

type TweetArgumentativeType = "attack" | "support" | "neutral" | "none";

type TweetPublicMetrics = {
  like_count: number;
  quote_count: number;
  reply_count: number;
  retweet_count: number;
};

type TweetNodeAttributes = {
  id: string;
  text: string;
  sentiment: TweetSentiment;
  argumentative_type: TweetArgumentativeType;
  acceptability: number;
  // public_metrics: TweetPublicMetrics;
  like_count: number;
  quote_count: number;
  reply_count: number;
  retweet_count: number;
};

type TweetNode = {
  name: string;
  attributes: TweetNodeAttributes;
  children: TweetNode[];
};

type TweetTreeMetrics = {
  general_sentiment: TweetSentiment;
  root_tweet_sentiment: TweetSentiment;
  sentiment_towards_root: TweetSentiment;
  root_tweet_argument_strength: number;
  strongest_argument_id: string;
};

type TweetTree = {
  tweet_tree: TweetNode;
  metrics: TweetTreeMetrics;
};

type TweetTreeAPIResponse = {
  response: TweetTree;
};
