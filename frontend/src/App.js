import React from "react";
import { ChakraProvider } from "@chakra-ui/react";
import ChatbotWidget from "./components/ChatbotWidget";

function App() {
  return (
    <ChakraProvider>
      <ChatbotWidget />
    </ChakraProvider>
  );
}

export default App;
