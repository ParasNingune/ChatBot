import React, { useState } from "react";
import {
  Box,
  IconButton,
  Input,
  InputGroup,
  InputRightElement,
  Text,
  VStack,
  Flex,
  Spinner,
} from "@chakra-ui/react";
import { ChatIcon, CloseIcon, ArrowForwardIcon } from "@chakra-ui/icons";
import axios from "axios";
import ChatMessage from "./ChatMessage";

const ChatbotWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [analyzing, setAnalyzing] = useState(false);

  const toggleChat = () => {
    if (!isOpen) {
      // Add greeting message when chat opens
      setMessages([
        {
          sender: "bot",
          text: "Hello! How may I help you today?",
          time: formatTime(),
        },
      ]);
    }
    setIsOpen(!isOpen);
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const formatTime = () => {
    const now = new Date();
    return now.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      sender: "user",
      text: input,
      time: formatTime(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    // Set analyzing state
    setAnalyzing(true);

    setTimeout(async () => {
      try {
        const response = await axios.post("http://localhost:5000/chat", {
          message: input,
        });

        const botMessage = {
          sender: "bot",
          text: response.data.answer,
          time: formatTime(),
        };
        setMessages((prev) => [...prev, botMessage]);
      } catch (error) {
        const botError = {
          sender: "bot",
          text: "Sorry, I couldn't process your request. Please try again.",
          time: formatTime(),
        };
        setMessages((prev) => [...prev, botError]);
      }

      // Stop analyzing state after response
      setAnalyzing(false);
    }, 5000); // Delay of 5 seconds
  };

  return (
    <Box position="fixed" bottom="4" right="4">
      {!isOpen ? (
        <IconButton
          icon={<ChatIcon />}
          colorScheme="blue"
          onClick={toggleChat}
          aria-label="Open Chat"
          isRound
          size={"lg"}
        />
      ) : (
        <Box
          w="350px"
          h="500px"
          bg="white"
          shadow="xl"
          rounded="2xl"
          borderWidth="1px"
          display="flex"
          flexDirection="column"
        >
          {/* Header */}
          <Flex
            justifyContent="space-between"
            alignItems="center"
            bg="blue.500"
            color="white"
            p="3"
            roundedTop="2xl"
          >
            <Text fontSize="lg" fontWeight="bold">
              NovaNectar Chatbot
            </Text>
            <IconButton
              icon={<CloseIcon />}
              size="sm"
              onClick={toggleChat}
              aria-label="Close Chat"
              variant="ghost"
              color="white"
              _hover={{
                bg: "red.500",
                shadow: "md",
              }}
            />
          </Flex>

          {/* Chat Area */}
          <VStack
            spacing="3"
            align="start"
            overflowY="auto"
            flex="1"
            p="4"
            bg="gray.50"
            roundedBottom="md"
          >
            {messages.map((message, index) => (
              <ChatMessage
                key={index}
                sender={message.sender}
                text={message.text}
                time={message.time}
              />
            ))}
            {/* Analyzing Animation */}
            {analyzing && (
              <Flex align="center" gap="2">
                <Spinner size="sm" color="blue.500" />
                <Text fontSize="sm" color="gray.600">
                  Analyzing...
                </Text>
              </Flex>
            )}
          </VStack>

          {/* Input Area */}
          <Box bg="gray.100" p="3" roundedBottom="2xl">
            <InputGroup size="md">
              <Input
                placeholder="Type your message..."
                value={input}
                onChange={handleInputChange}
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                bg="white"
                rounded="full"
                shadow="sm"
              />
              <InputRightElement>
                <IconButton
                  icon={<ArrowForwardIcon />}
                  size="sm"
                  onClick={sendMessage}
                  aria-label="Send Message"
                  colorScheme="blue"
                  rounded="full"
                  shadow="sm"
                />
              </InputRightElement>
            </InputGroup>
          </Box>
        </Box>
      )}
    </Box>
  );
};

export default ChatbotWidget;
