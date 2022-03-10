import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ChakraProvider, Box, Grid, theme } from "@chakra-ui/react";

import { ColorModeSwitcher } from "./ColorModeSwitcher";
import HomePage from "./pages/HomePage";
import TweetAnalysisPage from "./pages/TweetAnalysisPage";

export const App = () => (
  <ChakraProvider theme={theme}>
    <BrowserRouter>
      <Box textAlign="center" fontSize="xl">
        <Grid minH="100vh" p={3}>
          <ColorModeSwitcher justifySelf="flex-end" />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/analyze/:id" element={<TweetAnalysisPage />} />
          </Routes>
        </Grid>
      </Box>
    </BrowserRouter>
  </ChakraProvider>
);
