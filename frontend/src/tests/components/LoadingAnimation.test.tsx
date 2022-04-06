import React from "react";
import { render, screen } from "@testing-library/react";
import LoadingAnimation from "../../components/LoadingAnimation";

test("renders loading animation", () => {
  render(<LoadingAnimation />);
  const loadingAnimation = screen.getByTestId("spinner");
  expect(loadingAnimation).toBeInTheDocument();
});
