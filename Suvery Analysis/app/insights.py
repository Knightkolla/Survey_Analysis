import pandas as pd

def generate_insights(df):
    insights = []
    avg_sentiment = df['text_sentiment'].mean()
    avg_score = df['score_ratio'].mean()

    if avg_sentiment < 0 and avg_score < 0.6:
        insights.append("Students are struggling emotionally and with content. Consider revising lectures and improving engagement.")
    elif avg_sentiment > 0.2 and avg_score > 0.8:
        insights.append("Class is engaging and well-paced. No major changes needed.")

    if df['emoji_sentiment'].mean() < 0:
        insights.append("Emoji sentiment is trending negative. Check for emotional disengagement.")

    low_perf = df[df['score_ratio'] < 0.6]
    if not low_perf.empty:
        insights.append(f"{len(low_perf)} students scored below 60%. Consider offering remedial support.")

    region_perf = df.groupby('region')['score_ratio'].mean()
    lowest_region = region_perf.idxmin()
    if region_perf[lowest_region] < 0.6:
        insights.append(f"Students from the {lowest_region} region are underperforming. Consider regional support.")

    time_vs_score_corr = df['score_ratio'].corr(pd.to_timedelta(df['time_taken']).dt.total_seconds())
    if time_vs_score_corr < -0.3:
        insights.append("Students who took more time scored lower. Consider reviewing quiz complexity.")

    return insights

def generate_temporal_insights(df):
    insights = []
    df['date'] = df['timestamp'].dt.date
    trends = df.groupby('date').agg({
        'score_ratio': 'mean',
        'text_sentiment': 'mean',
        'emoji_sentiment': 'mean'
    }).reset_index()

    if len(trends) >= 2:
        score_diff = trends['score_ratio'].iloc[-1] - trends['score_ratio'].iloc[0]
        sentiment_diff = trends['text_sentiment'].iloc[-1] - trends['text_sentiment'].iloc[0]

        if score_diff < -0.1:
            insights.append("⚠️ Performance is declining over time. Possible issue with recent lectures or assessments.")
        elif score_diff > 0.1:
            insights.append("✅ Performance has improved recently. Teaching methods may be working well.")

        if sentiment_diff < -0.1:
            insights.append("😟 Student sentiment is becoming more negative. May need to check engagement.")
        elif sentiment_diff > 0.1:
            insights.append("😊 Sentiment is trending positively. Students seem more satisfied.")

    return insights
def generate_weekly_trend_insight(df):
    df['week'] = df['timestamp'].dt.isocalendar().week
    weekly_summary = df.groupby('week').agg({
        'score_ratio': 'mean',
        'text_sentiment': 'mean'
    }).reset_index()

    if len(weekly_summary) >= 2:
        last = weekly_summary.iloc[-1]
        prev = weekly_summary.iloc[-2]

        insights = []

        score_diff = last['score_ratio'] - prev['score_ratio']
        sent_diff = last['text_sentiment'] - prev['text_sentiment']

        if abs(score_diff) > 0.05:
            change = "increased" if score_diff > 0 else "decreased"
            insights.append(f"📈 Average score has {change} from {prev['score_ratio']:.2f} to {last['score_ratio']:.2f} over the last week.")

        if abs(sent_diff) > 0.05:
            change = "improved" if sent_diff > 0 else "declined"
            insights.append(f"💬 Sentiment has {change} from {prev['text_sentiment']:.2f} to {last['text_sentiment']:.2f} over the last week.")

        return insights
    return []