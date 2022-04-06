import React from "react";
import { Container } from "@chakra-ui/react";

import ErrorAlert from "../components/ErrorAlert";

const PageNotFound = () => {
  return (
    <Container data-testid="page-not-found">
      <ErrorAlert
        errorMessage="404 Not Found"
        errorTitle="Page not Found!"
        errorDescription="This page (route) does not exist! Try going back to the home page"
      />
    </Container>
  );
};

export default PageNotFound;
