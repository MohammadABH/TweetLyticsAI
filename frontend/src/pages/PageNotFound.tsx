import { Container } from "@chakra-ui/react";
import React from "react";

import ErrorAlert from "../components/ErrorAlert";

const PageNotFound = () => {
  return (
    <Container>
      <ErrorAlert
        errorMessage="404 Not Found"
        errorTitle="Page not Found!"
        errorDescription="This page (route) does not exist! Try going back to the home page"
      />
    </Container>
  );
};

export default PageNotFound;
