import React from "react";

interface IProps {
  tweets: TweetTree | null;
  errorMessage: string;
}

const TweetTree = ({ tweets, errorMessage }: IProps) => {
  if (tweets === null) {
    return <div>Loading</div>;
  }

  if (errorMessage !== "") {
    return <div>Error</div>;
  }

  console.log(tweets);
  return <div>Tweet Tree</div>;
};

export default TweetTree;
