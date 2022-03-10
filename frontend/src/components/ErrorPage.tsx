import React from "react";
import {
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from "@chakra-ui/react";

interface IProps {
  errorMessage: string;
}

const ErrorPage = ({ errorMessage }: IProps) => {
  return (
    <Alert
      status="error"
      variant="subtle"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      textAlign="center"
      height="200px"
    >
      <AlertIcon boxSize="40px" mr={0} />
      <AlertTitle mt={4} mb={1} fontSize="lg">
        Oops, something went wrong!
      </AlertTitle>
      <AlertDescription maxWidth="sm">
        Are you sure the Tweet URL you added is valid? Perhaps its deleted? Try
        another Tweet or come back later.
      </AlertDescription>
    </Alert>
  );
};

export default ErrorPage;
