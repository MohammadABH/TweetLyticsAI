import React from "react";
import { render, screen } from "@testing-library/react";
import PageNotFound from "../../pages/PageNotFound";

test("renders page not found page", async () => {
  render(<PageNotFound />);
  const pageNotFound = screen.getByTestId("page-not-found");
  expect(pageNotFound).toBeInTheDocument();
});
