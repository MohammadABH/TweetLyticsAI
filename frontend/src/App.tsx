import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ChakraProvider, Box, Grid, theme } from "@chakra-ui/react";

import HomePage from "./pages/HomePage";
import TweetAnalysisPage from "./pages/TweetAnalysisPage";
import Navbar from "./components/Navbar";
import PageNotFound from "./pages/PageNotFound";

export const App = () => {
  return (
    <ChakraProvider theme={theme}>
      <BrowserRouter>
        <Box textAlign="center" fontSize="xl" data-testid="app">
          <Grid minH="100vh" p={3}>
            <Box justifySelf="flex-end">
              <Navbar />
            </Box>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/home" element={<HomePage />} />
              <Route path="/analyze/:id" element={<TweetAnalysisPage />} />
              <Route path="*" element={<PageNotFound />} />
            </Routes>
          </Grid>
        </Box>
      </BrowserRouter>
    </ChakraProvider>
  );
};
