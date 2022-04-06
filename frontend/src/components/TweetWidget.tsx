import React from "react";
import { Text } from "@chakra-ui/react";
import { Tweet } from "react-twitter-widgets";

interface IProps {
  tweetId: string | undefined;
}

const TweetWidget = ({ tweetId }: IProps) => {
  if (tweetId === undefined) return <></>;

  return (
    <Tweet
      tweetId={tweetId}
      renderError={(_err) => <Text>"Could not load tweet!"</Text>}
    />
  );
};

export default TweetWidget;
