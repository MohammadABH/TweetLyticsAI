def preprocess(tweet):
    """
    Function that preprocesses the input tweet by removing user handles and http
    links

    :param tweet: the input tweet (text) to be preprocessed

    :return       pre-processed tweet
    """
    preprocessed_tweet = []
    original_tweet_words = tweet.split(" ")
    for word in original_tweet_words:
        word = 'http' if word.startswith('http') else word                  # Preprocess links
        word = '@user' if word.startswith('@') and len(word) > 1 else word  # Preprocess twitter handles

        preprocessed_tweet.append(word)  # Add the processed word to the list

    preprocessed_tweet_string = " ".join(preprocessed_tweet)
    return preprocessed_tweet_string


if __name__ == "__main__":
    pass
