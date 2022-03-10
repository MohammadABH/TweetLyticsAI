import React from "react";
import { Center, Container, Heading, VStack } from "@chakra-ui/react";
import ErrorPage from "./ErrorPage";
import LoadingAnimation from "./LoadingAnimation";
import TweetTreeMetrics from "./TweetTreeMetrics";
import TweetTreeVisualization from "./TweetTreeVisualization";

interface IProps {
  tweetId: string | undefined;
  tweets: TweetTree | null;
  errorMessage: string;
}

const TweetTree = ({ tweetId, tweets, errorMessage }: IProps) => {
  if (tweets === null) {
    return (
      <>
        <Heading as="h1" size="xl" p={2}>
          Please wait... Processing Tweet ID: {tweetId}
        </Heading>
        <Center>
          <LoadingAnimation />
        </Center>
      </>
    );
  }

  if (errorMessage !== "" || tweetId === undefined) {
    return (
      <Container>
        <ErrorPage errorMessage={errorMessage} />
      </Container>
    );
  }

  console.log(tweets);
  return (
    <>
      <Heading as="h1" size="xl" p={4}>
        Tweet Analysis Page! Reading Tweet ID: {tweetId}
      </Heading>
      <Center p={4}>
        <TweetTreeMetrics tweetId={tweetId} tweetTreeMetrics={tweets.metrics} />
      </Center>
      <VStack
        width="98vw"
        height="100vh"
        p={4}
        borderWidth="1px"
        borderRadius="lg"
      >
        <Heading as="h2" size="m" p={2}>
          Tweet Visualization
        </Heading>
        <TweetTreeVisualization tweetTree={tweets.tweet_tree} />
      </VStack>
    </>
  );
};

export default TweetTree;
