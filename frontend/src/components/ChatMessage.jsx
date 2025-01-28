import React from "react";
import { Box, Text, VStack } from "@chakra-ui/react";

const ChatMessage = ({ sender, text, time }) => {
  const isUser = sender === "user";

  return (
    <VStack
      align={isUser ? "end" : "start"}
      w="full"
      spacing="0"
      mb="4"
    >
      <Box
        bg={isUser ? "blue.500" : "gray.300"}
        color={isUser ? "white" : "black"}
        px="4"
        py="3"
        rounded="md"
        alignSelf={isUser ? "flex-end" : "flex-start"}
        shadow="md"
        maxW="75%"
      >
        <Text fontSize={"sm"}>{text}</Text>
      </Box>
      <Text fontSize="xs" color="gray.500">
        {time}
      </Text>
    </VStack>
  );
};

export default ChatMessage;
