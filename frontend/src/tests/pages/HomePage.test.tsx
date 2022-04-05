import React from "react";
import { BrowserRouter } from "react-router-dom";
import { createMemoryHistory } from "history";
import { render, screen } from "@testing-library/react";
import HomePage from "../../pages/HomePage";

test("renders home page", async () => {
  render(
    <BrowserRouter>
      <HomePage />
    </BrowserRouter>
  );
  const homePage = screen.getByTestId("home-page");
  expect(homePage).toBeInTheDocument();
});
