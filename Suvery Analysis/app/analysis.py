import pandas as pd
def correlation_analysis(df):
    return df[['emoji_sentiment', 'text_sentiment', 'score_ratio']].corr()

def get_low_performers(df):
    return df[df['score_ratio'] < 0.6]

def temporal_trends(df):
    df['date'] = df['timestamp'].dt.date
    trends = df.groupby('date').agg({
        'score_ratio': 'mean',
        'text_sentiment': 'mean',
        'emoji_sentiment': 'mean'
    }).reset_index()
    return trends

def regional_performance(df):
    return df.groupby('region')['score_ratio'].mean().reset_index().sort_values(by='score_ratio')

def gender_sentiment_score(df):
    return df.groupby('gender').agg({'score_ratio': 'mean', 'text_sentiment': 'mean'}).reset_index()

def time_vs_score(df):
    df['time_taken_seconds'] = pd.to_timedelta(df['time_taken']).dt.total_seconds()
    return df[['time_taken_seconds', 'score_ratio']]

