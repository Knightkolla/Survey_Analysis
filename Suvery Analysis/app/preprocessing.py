import pandas as pd
from textblob import TextBlob

def load_data(path):
    return pd.read_csv(path)

def preprocess(df):
    emoji_map = {"😊": 1, "😐": 0, "😡": -1}
    df['emoji_sentiment'] = df['emoji'].map(emoji_map)
    df['text_sentiment'] = df['feedback_text'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['score_ratio'] = df['score'] / df['total']
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df