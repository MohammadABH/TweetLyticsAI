import React from "react";
import {
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from "@chakra-ui/react";

interface IProps {
  errorMessage: string;
  errorTitle: string;
  errorDescription: string;
}

const ErrorAlert = ({ errorMessage, errorTitle, errorDescription }: IProps) => {
  return (
    <Alert
      status="error"
      variant="subtle"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      textAlign="center"
      height="200px"
			data-testid="error-alert"
    >
      <AlertIcon boxSize="40px" mr={0} />
      <AlertTitle mt={4} mb={1} fontSize="lg">
        {errorTitle}
      </AlertTitle>
      <AlertDescription maxWidth="sm">{errorDescription}</AlertDescription>
    </Alert>
  );
};

export default ErrorAlert;
