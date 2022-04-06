import React from "react";
import axios, { AxiosResponse } from "axios";
import { render, screen, act, waitFor } from "@testing-library/react";
import { Route, MemoryRouter, Routes } from "react-router-dom";
import example1 from "../../mock_data/example1.json";

import TweetAnalysisPage from "../../pages/TweetAnalysisPage";

jest.mock("axios");
const mockedAxios = axios as jest.Mocked<typeof axios>;

test("renders tweet analysis page", async () => {
  const mockedResponse: AxiosResponse = {
    data: example1,
    status: 200,
    statusText: "OK",
    headers: {},
    config: {},
  };
  mockedAxios.get.mockResolvedValueOnce(mockedResponse);

  await act(async () => {
    render(
      <MemoryRouter initialEntries={["/analyze/1"]}>
        <Routes>
          <Route path="/analyze/:id" element={<TweetAnalysisPage />} />
        </Routes>
      </MemoryRouter>
    );
  });
  waitFor(() => {
    const tweetAnalysisPage = screen.getByTestId("tweet-tree");
    expect(tweetAnalysisPage).toBeInTheDocument();
  });
});

test("renders tweet analysis example page", async () => {
  const mockedResponse: AxiosResponse = {
    data: example1,
    status: 200,
    statusText: "OK",
    headers: {},
    config: {},
  };
  mockedAxios.get.mockResolvedValueOnce(mockedResponse);
  await act(async () => {
    render(
      <MemoryRouter initialEntries={["/analyze/tweetExample1"]}>
        <Routes>
          <Route path="/analyze/:id" element={<TweetAnalysisPage />} />
        </Routes>
      </MemoryRouter>
    );
  });
  waitFor(() => {
    const tweetAnalysis = screen.getByTestId("success");
    expect(tweetAnalysis).toBeInTheDocument();
  });
});

test("renders loading component", async () => {
  await act(async () => {
    render(
      <MemoryRouter initialEntries={["/analyze/1"]}>
        <Routes>
          <Route path="/analyze/:id" element={<TweetAnalysisPage />} />
        </Routes>
      </MemoryRouter>
    );
  });
  waitFor(() => {
    const loading = screen.getByTestId("loading");
    expect(loading).toBeInTheDocument();
  });
});

test("renders error component", async () => {
  await act(async () => {
    render(<TweetAnalysisPage />);
  });
  waitFor(() => {
    const error = screen.getByTestId("error");
    expect(error).toBeInTheDocument();
  });
});
