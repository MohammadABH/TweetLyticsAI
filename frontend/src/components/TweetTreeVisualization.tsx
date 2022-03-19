import React, { useState } from "react";
import Tree from "react-d3-tree";
import { useDisclosure } from "@chakra-ui/react";

import TweetNodeInformation from "./TweetNodeInformation";

import "./custom-tree.css";

const handleNodeColor = (sentiment: string): string => {
  if (sentiment === "positive") return "green";
  else if (sentiment === "negative") return "red";
  else return "grey";
};

interface IProps {
  tweetTree: TweetNode;
}

const renderNodeWithCustomEvents = ({
  nodeDatum,
  toggleNode,
  handleNodeClick,
}: {
  nodeDatum: TweetNode;
  toggleNode: () => any;
  handleNodeClick: (data: TweetNode) => any;
}) => (
  <g>
    <circle
      r="15"
      onClick={() => handleNodeClick(nodeDatum)}
      color={handleNodeColor(nodeDatum.attributes.sentiment)}
      fill={handleNodeColor(nodeDatum.attributes.sentiment)}
    />
    <text fill="black" strokeWidth="1" x="20" onClick={toggleNode}>
      {nodeDatum.children && <>(Expand 👋) </>}
    </text>
  </g>
);

const TweetTreeVisualization = ({ tweetTree }: IProps) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [currentNode, setCurrentNode] = useState<TweetNode | null>(null);

  const getDynamicPathClass = (
    { source, target }: any,
    orientation: string
  ): string => {
    if (target.data.attributes.argumentative_type === "attack")
      return "link__attack";
    else if (target.data.attributes.argumentative_type === "support")
      return "link__support";
    else return "link__neutral";
  };

  const handleNodeClick = (tweetNode: TweetNode) => {
    setCurrentNode(tweetNode);
    console.log(currentNode?.attributes.sentiment);
    onOpen();
  };

  const handleCloseModal = () => {
    setCurrentNode(null);
    onClose();
  };

  return (
    <>
      <Tree
        zoom={1}
        orientation="vertical"
        pathFunc={"step"}
        data={tweetTree}
        renderCustomNodeElement={(rd3tProps: any) =>
          renderNodeWithCustomEvents({ ...rd3tProps, handleNodeClick })
        }
        pathClassFunc={getDynamicPathClass}
      />
      <TweetNodeInformation
        currentNode={currentNode}
        isOpen={isOpen}
        handleCloseModal={handleCloseModal}
        onOpen={onOpen}
      />
    </>
  );
};

export default TweetTreeVisualization;
