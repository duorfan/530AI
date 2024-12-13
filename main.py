import streamlit as st
from DesignTK_Final.openai_helpers import generate_response

st.title("OpenAI-Powered App")
st.write("This app interacts with OpenAI's GPT to generate responses.")

# User input
user_input = st.text_input("Enter your prompt:")

# Display the response
if st.button("Generate"):
    if user_input:
        with st.spinner("Generating response..."):
            response = generate_response(user_input)
        st.success("Generated Response:")
        st.write(response)
    else:
        st.error("Please enter a prompt!")
