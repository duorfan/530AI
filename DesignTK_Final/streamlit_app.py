import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.decomposition import PCA
import plotly.express as px
import openai
import os
from dotenv import load_dotenv

# Ensure this is the FIRST Streamlit command
st.set_page_config(page_title="Board Game Recommender", page_icon="🎲", layout="wide")

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_bgg_dataset.csv")
    # Parse lists
    def parse_list_column(col_value):
        if isinstance(col_value, str):
            col_value = col_value.strip('[]')
            if len(col_value) == 0:
                return []
            items = [x.strip().strip("'").strip('"') for x in col_value.split(',')]
            items = [x for x in items if x]
            return items
        return []
    df['Mechanics'] = df['Mechanics'].apply(parse_list_column)
    df['Domains'] = df['Domains'].apply(parse_list_column)
    return df

# Function to interact with OpenAI API
def get_ai_recommendations(filtered_games):
    game_names = filtered_games['Name'].tolist()
    prompt = f"""
    I have a list of board games: {', '.join(game_names)}. 
    Recommend online versions of these games or similar fun activities that could help maintain long-distance relationships. 
    Keep the tone humorous and casual.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a fun and humorous assistant who helps maintain long-distance relationships with creative ideas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"

# Load and process data
df = load_data()

all_mechanics = sorted(list(set(m for mechs in df['Mechanics'] for m in mechs)))
all_domains = sorted(list(set(d for doms in df['Domains'] for d in doms)))

mech_mlb = MultiLabelBinarizer(classes=all_mechanics)
dom_mlb = MultiLabelBinarizer(classes=all_domains)

mech_encoded = mech_mlb.fit_transform(df['Mechanics'])
dom_encoded = dom_mlb.fit_transform(df['Domains'])

X = np.hstack([mech_encoded, dom_encoded])

k = 7
kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
kmeans.fit(X)
df['Cluster'] = kmeans.labels_

# Dimensionality reduction for visualization
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X)
df['PC1'] = X_pca[:,0]
df['PC2'] = X_pca[:,1]

# STREAMLIT UI - Improved Design
st.title("🎲 Board Game Recommender")
st.markdown(
    """
    Welcome to the **Board Game Recommender**! 🎉 Explore games based on their mechanics or domains, 
    and find the perfect match for your next game night. Use the filters below to narrow down your choices.
    """
)

# Select tag type (Mechanics or Domains)
st.markdown("### 🔍 Filter by Tag Type")
tag_type = st.radio("Choose a tag type to filter:", ["Mechanics", "Domains"], horizontal=True)

# Generate the dropdown menu based on the selected tag type
with st.expander("Select Tag and Filters", expanded=True):
    if tag_type == "Mechanics":
        selected_tag = st.selectbox("🎯 Select a Mechanic:", all_mechanics)
        filtered_df = df[df['Mechanics'].apply(lambda x: selected_tag in x)]
    else:  # Domains
        selected_tag = st.selectbox("🎯 Select a Domain:", all_domains)
        filtered_df = df[df['Domains'].apply(lambda x: selected_tag in x)]

    # Display additional filters in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        min_players = st.slider("👥 Minimum players:", 1, 10, 2)
    with col2:
        max_playtime = st.slider("⏳ Maximum play time (minutes):", 10, 300, 180)
    with col3:
        min_rating = st.slider("⭐ Minimum rating:", 0.0, 10.0, 7.0)

# Apply additional filters
filtered_df = filtered_df[
    (filtered_df['Min Players'] <= min_players) &
    (filtered_df['Max Players'] >= min_players) &
    (filtered_df['Play Time'] <= max_playtime) &
    (filtered_df['Rating Average'] >= min_rating)
]

# Display results
st.markdown("### 🎮 Matching Games")
st.write(f"**Number of matching games:** {len(filtered_df)}")
if len(filtered_df) > 0:
    st.dataframe(filtered_df[['Name', 'Year Published', 'Min Players', 'Max Players', 'Play Time', 'Rating Average', 'Mechanics', 'Domains']].head(20))
else:
    st.warning("No matching games found. Try adjusting the filters!")

# Visualization Section
st.markdown("### 📊 Visualization")
st.write("See how the board games are clustered based on their mechanics and domains.")
fig = px.scatter(
    df, x='PC1', y='PC2', color='Cluster',
    hover_data=['Name', 'Year Published', 'Rating Average', 'Play Time'],
    title="Board Game Clusters",
)
st.plotly_chart(fig)

# AI Recommendations Section
st.markdown("### 🤖 AI-Powered Recommendations")
st.write("Let AI recommend fun online activities or games to help maintain long-distance relationships!")
if len(filtered_df) > 0:
    if st.button("✨ Get AI Recommendations"):
        with st.spinner("Fetching recommendations..."):
            ai_recommendations = get_ai_recommendations(filtered_df)
        st.success("Here are some recommendations:")
        st.write(ai_recommendations)
else:
    st.warning("No matching games found. Adjust the filters to get recommendations!")

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ using [Streamlit](https://streamlit.io) and OpenAI.")
