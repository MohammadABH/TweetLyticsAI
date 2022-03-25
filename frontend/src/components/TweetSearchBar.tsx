import React, { useState } from "react";
import { Formik, Form, Field } from "formik";
import {
  Button,
  Container,
  FormControl,
  FormLabel,
  Input,
  FormErrorMessage,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

const TweetSearchBar = () => {
  const [tweetId, setTweetId] = useState<string>("");
  const [isValidInput, setIsValidInput] = useState<boolean>(false);
  const navigate = useNavigate();

  const validateTweetURL = (value: string): string | undefined => {
    let error = undefined;

    const regex =
      /^(?:http(?:s)?:\/\/)?(?:www\.)?twitter\.com\/(?:[a-zA-Z0-9_]+)\/status\/(\d+)\/?$/gm;
    const matchString = regex.exec(value);

    if (!value) {
      error = "Tweet URL is required!";
      setIsValidInput(false);
    }

    if (matchString == null) {
      error =
        "Invalid Tweet URL! Did you copy the URL right? For example, 'twitter.com/user/status/123' is a valid URL";
      setIsValidInput(false);
    } else {
      const matchedId = matchString[1];
      setTweetId(matchedId);
      setIsValidInput(true);
    }

    return error;
  };

  const loadCachedExample = (tweetExample: string): void => {
    console.log(tweetExample);
    navigate(`/analyze/${tweetExample}`);
  };

  return (
    <Container maxW="container.xl">
      <Formik
        initialValues={{ tweetUrl: "" }}
        onSubmit={(values, actions) => {
          actions.setSubmitting(false);
          navigate(`/analyze/${tweetId}`);
        }}
      >
        {({ isSubmitting }) => (
          <Form>
            <Field name="tweetUrl" validate={validateTweetURL}>
              {({ field, form }: any) => (
                <FormControl
                  isInvalid={form.errors.tweetUrl && form.touched.tweetUrl}
                >
                  <FormLabel htmlFor="tweetUrl">
                    Tweet URL / Tweet Link
                  </FormLabel>
                  <Input
                    {...field}
                    id="tweetUrl"
                    placeholder="Insert your Tweet URL here..."
                  />
                  <FormErrorMessage>{form.errors.tweetUrl}</FormErrorMessage>
                </FormControl>
              )}
            </Field>
            <Button
              mt={4}
              colorScheme="teal"
              isLoading={isSubmitting}
              type="submit"
              isDisabled={!isValidInput}
            >
              Analyze
            </Button>
          </Form>
        )}
      </Formik>
      <Container p={4}>
        <Button
          colorScheme="blue"
          p={2}
          m={2}
          onClick={() => loadCachedExample("tweetExample1")}
        >
          Example 1
        </Button>
        <Button
          colorScheme="blue"
          p={2}
          m={2}
          onClick={() => loadCachedExample("tweetExample2")}
        >
          Example 2
        </Button>
        <Button
          colorScheme="blue"
          p={2}
          m={2}
          onClick={() => loadCachedExample("tweetExample3")}
        >
          Example 3
        </Button>
      </Container>
    </Container>
  );
};

export default TweetSearchBar;
