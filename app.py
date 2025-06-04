import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load summaries
df = pd.read_csv("local_summaries.csv")
df = df.dropna(subset=["summary"])

# Load YouTube URLs
url_df = pd.read_csv("episode_urls.csv")

# Merge summaries with URLs
df = df.merge(url_df, on="title", how="left")

# Streamlit app setup
st.set_page_config(page_title="Lex Fridman Podcast Summaries", layout="wide")
st.title("🎧 Lex Fridman Podcast Summaries")

# Search box
search_query = st.text_input("🔍 Search for a topic or guest name:")

# Filter episodes
if search_query:
    filtered_df = df[df["title"].str.contains(search_query, case=False) | df["summary"].str.contains(search_query, case=False)]
    if filtered_df.empty:
        st.warning("No episodes found matching your search.")
        st.stop()
else:
    filtered_df = df

# Episode selector
selected_title = st.selectbox("Choose an episode:", filtered_df["title"].tolist())

# Show summary
selected_row = filtered_df[filtered_df["title"] == selected_title].iloc[0]
summary = selected_row["summary"]
url = selected_row.get("url", "")

st.subheader("📝 Summary")
st.write(summary)

# Word cloud
st.subheader("☁️ Word Cloud (from this summary)")
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(summary)
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# YouTube embed
st.subheader("▶️ Listen to Episode")
if isinstance(url, str) and "youtube.com/watch" in url:
    # Convert to embeddable format
    video_id = url.split("v=")[-1]
    st.video(f"https://www.youtube.com/embed/{video_id}")
else:
    st.info("🔗 Video not available.")
