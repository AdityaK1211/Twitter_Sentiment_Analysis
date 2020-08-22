import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import GetOldTweets3 as got


def sentiment_analyze(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    neg = score['neg']
    pos = score['pos']
    if neg > pos:
        print('Feedback: Negative')
    elif pos > neg:
        print('Feedback: Positive')
    else:
        print('Feedback: Neutral')


def get_tweets(input_search):
    print('Searching Tweets...')
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(input_search) \
        .setSince("2020-06-01") \
        .setUntil("2020-10-31") \
        .setMaxTweets(1000)
    # Creation of list that contains all tweets
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    # Creating list of chosen tweet data
    text_tweets = [[tweet.text] for tweet in tweets]
    return text_tweets


# Main
input_search = input('Enter Search: ')
text = ""
text_tweets = get_tweets(input_search)
length = len(text_tweets)
for i in range(0, length):
    text = text_tweets[i][0] + " " + text
    # print(text)

# Removes Punctuations
clean_text = text.translate(str.maketrans('', '', string.punctuation))
# print(clean_text)

# Tokenization
tokenized_text = word_tokenize(clean_text, 'english')
# print(tokenized_text)

# Stop Words
final_text = []
for word in tokenized_text:
    if word not in stopwords.words('english'):
        final_text.append(word)
# print(final_text)

# NLP Emotional Sentiment Analysis
emotion_list = []
with open('emotions.txt', 'r') as file:
    for line in file:
        line = line.replace('\n', '').replace(',', '').replace("'", '').strip()
        word, emotion = line.split(':')

        if word in final_text:
            emotion_list.append(emotion)
print(emotion_list)
emotion_list = Counter(emotion_list)

# Positive Negative Polarity
sentiment_analyze(clean_text)

# Graph of Emotions
fig, ax1 = plt.subplots()
ax1.bar(emotion_list.keys(), emotion_list.values())
fig.autofmt_xdate()
plt.savefig('emotion_graph.png')
plt.show()