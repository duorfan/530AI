#Board Game Recommender with AI Integration
This project is a web app that helps users find board games based on their preferences and discover fun, online activities for long-distance relationships using an AI-powered recommendation feature.

How to Use
1. Prerequisites
Install Python 3.9+
Install dependencies:
bash
Copy code
pip install -r requirements.txt
2. Add Your OpenAI API Key
Create a file named .env in the project directory.
Add your OpenAI API key in the following format:
makefile
Copy code
OPENAI_API_KEY=your_openai_api_key_here
3. Run the App
Launch the Streamlit app:
bash
Copy code
streamlit run streamlit_app.py
4. Access the Web App
Open the URL provided in the terminal (usually http://localhost:8501).
Features
Filter Board Games: Search by mechanics, domains, players, playtime, and ratings.
AI Recommendations: Suggests creative online activities using OpenAI’s API.
Interactive Visualizations: Displays clustered games for easy exploration.
File Structure
streamlit_app.py: Main web app script.
requirements.txt: List of dependencies.
cleaned_bgg_dataset.csv: Dataset of board games.
Note
This app requires an OpenAI API key to function. Make sure to add your .env file before running the app.
