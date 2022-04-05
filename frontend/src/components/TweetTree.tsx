import React from "react";
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
          Help! How can I unserstand the visualisation better?
        </Button>
        <Modal onClose={onClose} size="xl" isOpen={isOpen}>
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>
              How can I unserstand the visualisation better?
            </ModalHeader>
            <ModalCloseButton />
            <ModalBody>Don't Worry!</ModalBody>
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
