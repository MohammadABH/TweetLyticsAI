import React from "react";
import { Spinner, extendTheme } from "@chakra-ui/react";

const LoadingAnimation = () => {
  return (
    <Spinner
      thickness="4px"
      speed="0.65s"
      emptyColor="gray.200"
      color="blue.500"
      size="xl"
    />
  );
};

export default LoadingAnimation;