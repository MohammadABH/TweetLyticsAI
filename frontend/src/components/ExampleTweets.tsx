import React from "react";
import { Button, Container } from "@chakra-ui/react";

const ExampleTweets = () => {
  return (
    <Container>
      <Button colorScheme="blue" p={2} m={2}>
        Example 1
      </Button>
      <Button colorScheme="blue" p={2} m={2}>
        Example 2
      </Button>
      <Button colorScheme="blue" p={2} m={2}>
        Example 3
      </Button>
    </Container>
  );
};

export default ExampleTweets;
