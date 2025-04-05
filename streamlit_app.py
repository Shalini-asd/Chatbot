import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app in Telugu
st.title("ఆరోగ్య లక్షణాల తనిఖీదారు")  # "Shalini's BOT" in Telugu

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Collect user input for symptoms in Telugu
user_input = st.chat_input("మీ లక్షణాలను ఇక్కడ వివరించండి...")  # "Describe your symptoms here..." in Telugu

# Function to get a response from OpenAI with health advice in Telugu
def get_response(prompt):
    # Include a system message to ensure responses are in Telugu
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "మీరు ఇచ్చిన ప్రతి సమాధానం తెలుగులో ఉండాలి."},  # Ensure responses are in Telugu
            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            {"role": "user", "content": prompt}
        ]
    )
    # Access the content directly as an attribute
    return response.choices[0].message.content

# Process and display response if there's input
if user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant's response
    assistant_prompt = f"వినివిచ్చేవారు ఈ క్రింది లక్షణాలను నివేదించారు: {user_input}. ఒక సాధారణ సూచన లేదా సలహా ఇవ్వండి."
    assistant_response = get_response(assistant_prompt)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
