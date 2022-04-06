import React, { useState } from "react";
import {
  Center,
  Container,
  Heading,
  VStack,
  Link,
  Button,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  useDisclosure,
  OrderedList,
  ListItem,
} from "@chakra-ui/react";
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
  const { isOpen, onOpen, onClose } = useDisclosure();

  if (errorMessage !== "" || tweetId === undefined) {
    return (
      <Container data-testid="error">
        <ErrorAlert
          errorMessage={errorMessage}
          errorTitle="Oops, something went wrong!"
          errorDescription={`Are you sure the Tweet URL you added is valid? Perhaps its deleted? Try
					another Tweet or come back later. ${tweetId}`}
        />
      </Container>
    );
  }

  if (tweets === null) {
    return (
      <>
        <Heading as="h1" size="xl" p={2} data-testid="loading">
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
      <Heading as="h1" size="xl" p={4} data-testid="success">
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
        <Button colorScheme="teal" p={2} onClick={onOpen}>
          Help! How can I understand the visualisation better?
        </Button>
        <Modal
          onClose={onClose}
          size="xl"
          isOpen={isOpen}
          scrollBehavior="outside"
          isCentered
        >
          <ModalOverlay />
          <ModalContent>
            <ModalHeader textAlign="center">
              How can I understand the visualisation better?
            </ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              The visualisation you see below follows a tree structure, kind of
              like a family tree! Each circle (called a 'node') represents a
              tweet. The lines between each circle/node/tweet mean someone is
              replying to the other circle/node/tweet. For example, if someone
              tweets "I love Pizza", and someone replies "I love Pizza as well",
              then there will be a line from the latter circle to the former,
              and the latter circle will be one level under. The visualisation
              is also scrollable and draggable, try it yourself!
              <br />
              <br />
              You can click on nodes to see more details about the tweet from an
              expanded view.
              <br />
              <br />
              For nodes with replies, you can collapse/expand its replies by
              clicking the "(Expand / Collapse 👋)" button
              <br />
              <br />
              The colors of the circles represent the tweet's sentiment
              extracted from the text (sentiment means opionion expressed). The
              meaning of the colors:
              <br />
              <br />
              <OrderedList>
                <ListItem>
                  Circles that are red mean that the tweet has a negative
                  sentiment.
                </ListItem>
                <ListItem>
                  Circles that are green mean that the tweet has a positive
                  sentiment.
                </ListItem>
                <ListItem>
                  Circles that are grey mean that the tweet has a neutral
                  sentiment.
                </ListItem>
              </OrderedList>
              <br />
              <br />
              The colors of the lines/edges represent the tweet's argumentative
              stance towards the tweet its replying to, as one of
              {" {attack, support, neutral}"}. The meaning of the colors:
              <br />
              <br />
              <OrderedList>
                <ListItem>
                  Red egdes means the tweet is attacking its parent (parent is
                  the tweet its replying to)
                </ListItem>
                <ListItem>
                  Green egdes means the tweet is supporting its parent
                </ListItem>
                <ListItem>
                  Grey egdes means the tweet is neutral to its parent
                </ListItem>
              </OrderedList>
            </ModalBody>
            <ModalFooter>
              <Button onClick={onClose}>Close</Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
        <TweetTreeVisualization tweetTree={tweets.tweet_tree} />
      </VStack>
    </>
  );
};

export default TweetTree;
