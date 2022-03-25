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
        word = 'http' if tweet.startswith('http') else word  # Preprocess links
        word = '@user' if tweet.startswith('@') and len(word) > 1 else word  # Preprocess twitter handles
        preprocessed_tweet.append(word)
    return " ".join(preprocessed_tweet)
