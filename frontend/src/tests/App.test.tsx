import React from "react";
import { screen } from "@testing-library/react";
import { render } from "./test-utils";
import { App } from "../App";

test("renders main app", () => {
  render(<App />);
  const app = screen.getByTestId("app");
  expect(app).toBeInTheDocument();
});
