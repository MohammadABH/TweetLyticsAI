import React from "react";
import axios, { AxiosResponse } from "axios";

import { fetchTweetsApi, fetchCachedTweets } from "../../api/FetchTweets";
import example1 from "../../mock_data/example1.json";
import example2 from "../../mock_data/example2.json";
import example3 from "../../mock_data/example3.json";

jest.mock("axios");
const mockedAxios = axios as jest.Mocked<typeof axios>;

test("returns api 200 response", async () => {
  const mockedResponse: AxiosResponse = {
    data: example1,
    status: 200,
    statusText: "OK",
    headers: {},
    config: {},
  };
  mockedAxios.get.mockResolvedValueOnce(mockedResponse);

  const res = await fetchTweetsApi("123");
  expect(axios.get).toHaveBeenCalled();
});

test("returns api 400 response", async () => {
  const mockedResponse: AxiosResponse = {
    data: {},
    status: 400,
    statusText: "oops",
    headers: {},
    config: {},
  };
  mockedAxios.get.mockResolvedValueOnce(mockedResponse);

  const res = await fetchTweetsApi("123");
  expect(axios.get).toHaveBeenCalled();
});

test("returns api 500 response", async () => {
  const mockedResponse: AxiosResponse = {
    data: {},
    status: 400,
    statusText: "internal server errror",
    headers: {},
    config: {},
  };
  mockedAxios.get.mockResolvedValueOnce(mockedResponse);

  const res = await fetchTweetsApi("123");
  expect(axios.get).toHaveBeenCalled();
});

test("returns cached example tweet 1", async () => {
  const res = await fetchCachedTweets("tweetExample1");
  expect(res).toBe(example1);
});

test("returns cached example tweet 2", async () => {
  const res = await fetchCachedTweets("tweetExample2");
  expect(res).toBe(example2);
});

test("returns cached example tweet 3", async () => {
  const res = await fetchCachedTweets("tweetExample3");
  expect(res).toBe(example3);
});
