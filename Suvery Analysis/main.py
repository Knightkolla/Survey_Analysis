import streamlit as st
from app.preprocessing import load_data, preprocess
from app.insights import generate_insights, generate_temporal_insights
from app.dashboard import display_dashboard

def main():
    df = load_data("/Users/kartikeya/Documents/Suvery Analysis/data/sample_data.csv")
    df = preprocess(df)
    filtered_df = display_dashboard(df)
    insights = generate_insights(filtered_df) + generate_temporal_insights(filtered_df)

    st.write("### Key Insights for Selected Dates")
    for ins in insights:
        st.success(ins)

if __name__ == '__main__':
    main()