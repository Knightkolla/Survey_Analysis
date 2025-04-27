from app.preprocessing import load_data, preprocess
from app.dashboard import display_dashboard

def main():
    df = load_data("/Users/kartikeya/Documents/Suvery Analysis/data/sample_data.csv")
    df = preprocess(df)
    display_dashboard(df, [])

if __name__ == '__main__':
    main()