import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import HomeButton from "../../components/HomeButton";

test("renders home button", () => {
  const buttonSpy = jest.fn();
  render(<HomeButton onClick={buttonSpy} />);
  const homeButton = screen.getByTestId("home-button");
  expect(homeButton).toBeInTheDocument();
});

test("clicks home button", () => {
  const buttonSpy = jest.fn();
  render(<HomeButton onClick={buttonSpy} />);
  const homeButton = screen.getByTestId("home-button");

  fireEvent.click(homeButton);

  expect(buttonSpy).toHaveBeenCalled();
});
