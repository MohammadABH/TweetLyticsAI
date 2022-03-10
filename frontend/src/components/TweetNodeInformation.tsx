import React from "react";
import {
  Button,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  UnorderedList,
  ListItem,
} from "@chakra-ui/react";

interface IProps {
  currentNode: TweetNode | null;
  isOpen: boolean;
  onOpen: () => void;
  handleCloseModal: () => void;
}

const TweetNodeInformation = ({
  currentNode,
  isOpen,
  onOpen,
  handleCloseModal,
}: IProps) => {
  return (
    <Modal onClose={handleCloseModal} isOpen={isOpen} isCentered>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader alignSelf={"center"}>Tweet Data</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <UnorderedList>
            <ListItem>
              <strong>ID:</strong> {currentNode?.attributes.id}
            </ListItem>
            <ListItem>
              <strong>Text:</strong> "{currentNode?.attributes.text}"
            </ListItem>
            <ListItem>
              <strong>Sentiment:</strong> {currentNode?.attributes.sentiment}
            </ListItem>
            <ListItem>
              <strong>Argumentative Type:</strong>{" "}
              {currentNode?.attributes.argumentative_type}
            </ListItem>
            <ListItem>
              <strong>Argument Strength (Acceptability Degree): </strong>
              {currentNode?.attributes.acceptability === undefined
                ? "Not an argument"
                : currentNode?.attributes.acceptability}
            </ListItem>
            <ListItem>
              <strong>Like Count:</strong> {currentNode?.attributes.like_count}
            </ListItem>
            <ListItem>
              <strong>Retweet Count:</strong>{" "}
              {currentNode?.attributes.retweet_count}
            </ListItem>
            <ListItem>
              <strong>Reply Count:</strong>{" "}
              {currentNode?.attributes.reply_count}
            </ListItem>
          </UnorderedList>
        </ModalBody>
        <ModalFooter>
          <Button onClick={handleCloseModal}>Close</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
};

export default TweetNodeInformation;
