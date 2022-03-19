import React from "react";
import {
  Stat,
  StatGroup,
  StatLabel,
  StatHelpText,
  StatNumber,
  Heading,
  Icon,
  Tooltip,
  Box,
  Link,
} from "@chakra-ui/react";
import { ExternalLinkIcon } from "@chakra-ui/icons";
import { BiHappy, BiSad } from "react-icons/bi";
import { MdOutlineSentimentNeutral } from "react-icons/md";
import { AiOutlineInfoCircle } from "react-icons/ai";

interface IProps {
  tweetId: string;
  tweetTreeMetrics: TweetTreeMetrics;
}

const TweetTreeMetrics = ({ tweetTreeMetrics, tweetId }: IProps) => {
  const {
    general_sentiment,
    root_tweet_sentiment,
    sentiment_towards_root,
    root_tweet_argument_strength,
    strongest_argument_id,
  } = tweetTreeMetrics;

  const getSentimentMapping = (sentiment: string) => {
    if (sentiment === "positive")
      return <Icon as={BiHappy} color="green.500" w={8} h={8} />;
    else if (sentiment === "negative")
      return <Icon as={BiSad} color="red.500" w={8} h={8} />;
    else return <Icon as={MdOutlineSentimentNeutral} w={8} h={8} />;
  };
  return (
    <Box borderWidth="1px" borderRadius="lg" p={2} w="90%">
      <Heading as="h2" size="m" p={2}>
        Tweet Tree Metrics
      </Heading>
      <StatGroup p={2}>
        <Stat>
          <Tooltip
            label="General sentiment of all Tweets in the conversartion / tree"
            fontSize="md"
            placement="top"
          >
            <span>
              <Icon as={AiOutlineInfoCircle} w={6} h={6} />
            </span>
          </Tooltip>
          <StatLabel>General Sentiment</StatLabel>
          <StatNumber>{general_sentiment}</StatNumber>
          <StatHelpText>{getSentimentMapping(general_sentiment)}</StatHelpText>
        </Stat>

        <Stat>
          <Tooltip
            label="The sentiment of the original Tweet (the one inputted in the home page)"
            fontSize="md"
            placement="top"
          >
            <span>
              <Icon as={AiOutlineInfoCircle} w={6} h={6} />
            </span>
          </Tooltip>
          <StatLabel>Original Tweet Sentiment</StatLabel>
          <StatNumber>{root_tweet_sentiment}</StatNumber>
          <StatHelpText>
            {getSentimentMapping(root_tweet_sentiment)}
          </StatHelpText>
        </Stat>

        <Stat>
          <Tooltip
            label="The sentiment of all the Tweets directly replying to the original Tweet"
            fontSize="md"
            placement="top"
          >
            <span>
              <Icon as={AiOutlineInfoCircle} w={6} h={6} />
            </span>
          </Tooltip>
          <StatLabel>Sentiment Towards Original Tweet</StatLabel>
          <StatNumber>{sentiment_towards_root}</StatNumber>
          <StatHelpText>{getSentimentMapping(general_sentiment)}</StatHelpText>
        </Stat>

        <Stat>
          <Tooltip
            label="The Tweet that has the strongest argument. This argument was calculated using an algorithm called Exponent Based Semantics on Weighted Bipolar Argumentation Frameworks"
            fontSize="md"
            placement="top"
          >
            <span>
              <Icon as={AiOutlineInfoCircle} w={6} h={6} />
            </span>
          </Tooltip>
          <StatLabel>Strongest Argument</StatLabel>
          <StatNumber>
            <Link
              href={`https://twitter.com/twitter/status/${tweetId}`}
              isExternal
            >
              <u>{strongest_argument_id}</u> <ExternalLinkIcon mx="2px" />
            </Link>
          </StatNumber>
        </Stat>

        <Stat>
          <Tooltip
            label="The numeric strength score of the strongest argument in the conversation / tree"
            fontSize="md"
            placement="top"
          >
            <span>
              <Icon as={AiOutlineInfoCircle} w={6} h={6} />
            </span>
          </Tooltip>
          <StatLabel>Original Tweet Argument Strength</StatLabel>
          <StatNumber>{root_tweet_argument_strength}</StatNumber>
        </Stat>
      </StatGroup>
    </Box>
  );
};

export default TweetTreeMetrics;
