import React from "react";
import { render, screen } from "@testing-library/react";
import ErrorAlert from "../../components/ErrorAlert";

test("renders error alert", () => {
  render(
    <ErrorAlert
      errorMessage="Error"
      errorTitle="Error Title"
      errorDescription="Error description"
    />
  );
  const errorAlert = screen.getByTestId("error-alert");
  expect(errorAlert).toBeInTheDocument();
});
