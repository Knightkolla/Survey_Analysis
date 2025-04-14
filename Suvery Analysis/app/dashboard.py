import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from app.analysis import temporal_trends, regional_performance, gender_sentiment_score, time_vs_score

def display_dashboard(df):
    st.set_page_config(page_title="Survey + Quiz Analysis Dashboard", layout="wide")
    st.title("📊 Survey + Quiz Analysis Dashboard")

    st.sidebar.write("## Filter Results by Date")
    start_date = st.sidebar.date_input("Start Date", df['timestamp'].min().date())
    end_date = st.sidebar.date_input("End Date", df['timestamp'].max().date())

    filtered_df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

    st.write("### Survey and Quiz Data")
    st.dataframe(filtered_df)

    st.write("### Sentiment vs Score")
    fig, ax = plt.subplots()
    sns.scatterplot(x=filtered_df['text_sentiment'], y=filtered_df['score_ratio'], hue=filtered_df['emoji_sentiment'], ax=ax, palette='coolwarm')
    ax.set_xlabel("Text Sentiment")
    ax.set_ylabel("Score Ratio")
    st.pyplot(fig)

    st.write("### Trends Over Time")
    trend_data = temporal_trends(filtered_df)
    fig2, ax2 = plt.subplots()
    sns.lineplot(data=trend_data, x='date', y='score_ratio', label='Score Ratio', ax=ax2)
    sns.lineplot(data=trend_data, x='date', y='text_sentiment', label='Text Sentiment', ax=ax2)
    sns.lineplot(data=trend_data, x='date', y='emoji_sentiment', label='Emoji Sentiment', ax=ax2)
    ax2.set_ylabel("Value")
    st.pyplot(fig2)

    st.write("### Regional Performance")
    region_df = regional_performance(filtered_df)
    fig3, ax3 = plt.subplots()
    sns.barplot(data=region_df, x='region', y='score_ratio', ax=ax3)
    ax3.set_ylabel("Average Score Ratio")
    st.pyplot(fig3)

    st.write("### Gender-Based Summary")
    gender_df = gender_sentiment_score(filtered_df)
    st.dataframe(gender_df)

    st.write("### Time Taken vs Score")
    time_score_df = time_vs_score(filtered_df)
    fig4, ax4 = plt.subplots()
    sns.scatterplot(data=time_score_df, x='time_taken_seconds', y='score_ratio', ax=ax4)
    ax4.set_xlabel("Time Taken (seconds)")
    ax4.set_ylabel("Score Ratio")
    st.pyplot(fig4)

    return filtered_df