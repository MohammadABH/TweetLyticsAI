import React from "react";
import {
  Heading,
  Text,
  Container,
  UnorderedList,
  ListItem,
} from "@chakra-ui/react";

import TweetSearchBar from "../components/TweetSearchBar";

const HomePage = () => {
  return (
    <>
      <Heading as="h1" size="4xl">
        TweetLyticsAI
      </Heading>
      <TweetSearchBar />
      <Container
        maxW="container.lg"
        borderWidth="1px"
        borderRadius="lg"
        overflow="hidden"
        p={10}
        maxH="container.sm"
        height="80%"
      >
        <Text>
          Input a Tweet URL above to see how other users are interacting with a
          Tweet both directly and indirectly! Specifically, how are they arguing
          with the tweet? Are people supporting the tweet? Are they attacking
          it? What is the sentiment towards the tweet (positive / negative /
          neutral)? Who is winning the argument? Is the original tweet winning?
          This application will perform all this analysis for you NOW!
        </Text>
      </Container>

      <Container>
        <strong>Note:</strong>
        <UnorderedList>
          <ListItem>
            Directly means when someone directly replied to the tweet
          </ListItem>
          <ListItem>
            Indirectly means when someone tweets something related to the topic
            of the tweet and is an argument for / against the tweet
          </ListItem>
        </UnorderedList>
      </Container>
    </>
  );
};

export default HomePage;
