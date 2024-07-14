import streamlit as st
import praw
from datetime import datetime

def get_reddit_videos(subreddit_name, limit=50):
    reddit = praw.Reddit(
        client_id=st.secrets["REDDIT_CLIENT_ID"],
        client_secret=st.secrets["REDDIT_CLIENT_SECRET"],
        user_agent=st.secrets["REDDIT_USER_AGENT"]
    )
    subreddit = reddit.subreddit(subreddit_name)
    videos = []
    try:
        for submission in subreddit.hot(limit=limit):
            if submission.is_video:
                videos.append({
                    "title": submission.title,
                    "reddit_url": f"https://www.reddit.com{submission.permalink}" ,
                    "video_url": submission.media["reddit_video"]["fallback_url"],
                    "timestamp": submission.created_utc
                })
    except Exception as e:
        st.error(f"Error Fetching Videos: {e}")
    return videos

def display_videos(videos):
    for video in videos:
        with st.container():
            st.subheader(video["title"])
            video_html = f'<video src="{video["video_url"]}" width="480" height="270" controls></video>'
            st.markdown(video_html, unsafe_allow_html=True)
            st.markdown(f"Reddit Video Page: [Link to Reddit]({video['reddit_url']})")
            timestamp = datetime.utcfromtimestamp(video['timestamp'])
            st.write(f"Posted on: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    st.set_page_config(page_title = "Reddit Videos Fetcher", layout="wide")
    st.title("Reddit Videos Fetcher")

    container = st.container()
    with container:
        st.sidebar.title(" ")
        subreddit_name = st.sidebar.text_input("Enter Subreddit Name:")

        if subreddit_name.strip() == "":
            st.warning("Please Enter a Subreddit Name.")
            return
    
        videos = get_reddit_videos(subreddit_name)

        if not videos:
            st.warning(f"No recently shared videos found in the subreddit '{subreddit_name}'")
        else:
            st.subheader(f"Showing videos from subreddit '{subreddit_name}'")
            display_videos(videos)

if __name__ == "__main__":
    main()