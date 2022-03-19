import React from "react";
import { Center, Container, Heading, VStack, Link } from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";

import ErrorAlert from "./ErrorAlert";
import LoadingAnimation from "./LoadingAnimation";
import TweetTreeMetrics from "./TweetTreeMetrics";
import TweetTreeVisualization from "./TweetTreeVisualization";
import TweetWidget from "./TweetWidget";

interface IProps {
  tweetId: string | undefined;
  tweets: TweetTree | null;
  errorMessage: string;
}

const TweetTree = ({ tweetId, tweets, errorMessage }: IProps) => {
  if (errorMessage !== "" || tweetId === undefined) {
    return (
      <Container>
        <ErrorAlert
          errorMessage={errorMessage}
          errorTitle="Oops, something went wrong!"
          errorDescription="Are you sure the Tweet URL you added is valid? Perhaps its deleted? Try
					another Tweet or come back later."
        />
      </Container>
    );
  }

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

  return (
    <>
      <Heading as="h1" size="xl" p={4}>
        Tweet Analysis Page! Reading Tweet ID:{" "}
        <Link href={`https://twitter.com/twitter/status/${tweetId}`} isExternal>
          <u>{tweetId}</u> <ExternalLinkIcon mx="2px" />
        </Link>
      </Heading>
      <Container p={4}>
        <TweetWidget tweetId={tweetId} />
      </Container>
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
