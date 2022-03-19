import React from "react";
import { IconButton } from "@chakra-ui/react";
import { AiOutlineHome } from "react-icons/ai";

interface IProps {
  onClick: () => void;
}

const HomeButton = ({ onClick }: IProps) => {
  return (
    <IconButton
      aria-label="Navigate to Home Page"
      icon={<AiOutlineHome />}
      justifySelf="flex-start"
      size="md"
      fontSize="lg"
      variant="ghost"
      color="current"
      marginLeft="2"
      onClick={onClick}
    />
  );
};

export default HomeButton;
