import React from "react";
import { render, screen } from "@testing-library/react";
import ColorModeSwitcher from "../../components/ColorModeSwitcher";

test("renders color picker", () => {
  render(<ColorModeSwitcher />);
  const colorModeSwitcher = screen.getByTestId("color-picker");
  expect(colorModeSwitcher).toBeInTheDocument();
});
