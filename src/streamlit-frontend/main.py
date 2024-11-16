import streamlit as st
import requests

# Set the backend URL
backend_url = "http://127.0.0.1:8000"

def fetchOptions():
    a = requests.get(backend_url + "/options")
    if a.status_code == 200:
        return a.json()
    else:
        return {"error": True}

def fetchImageUrls(option):
    a = requests.get(f"{backend_url}/images/{option}")
    return a.json()

def send_message_to_api(user_message, image_urls):
    """
    Sends the user message and selected image URLs to the backend API and returns the assistant's response.
    """
    try:
        response = requests.post(
            backend_url + "/chat",
            json={
                "message": user_message,
                "image_urls": image_urls,
            },
        )
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return response.json().get("response", "Sorry, I didn't understand that.")
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Initialize the chat history in session state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # List of dicts: {"role": "user"|"assistant", "text": "..."}

# Fetch options from the backend
options = fetchOptions()

# Initialize session state for the selected option
if "selected_option" not in st.session_state:
    st.session_state["selected_option"] = options[0]  # Default to the first option

# Page Title
st.title("Streamlit Frontend with FastAPI Backend")

st.write("This is a simple chatbot with image sets.")

# Dropdown with session state
selected_option = st.selectbox(
    'Select an image set',
    options,
    index=options.index(st.session_state["selected_option"]) if st.session_state["selected_option"] in options else 0,
    key="selected_option"
)

# Fetch image URLs based on the selected option
imageUrls = fetchImageUrls(st.session_state["selected_option"]).get("image_set", [])

# Display images
if imageUrls:
    st.subheader("Selected Image Set")
    cols = st.columns(len(imageUrls))
    for i, image_path in enumerate(imageUrls):
        with cols[i]:
            st.image(image_path, use_container_width=True)

# Chat functionality
st.subheader("Chat")
for entry in st.session_state["chat_history"]:
    with st.chat_message(entry["role"]):
        st.markdown(entry["text"])

# User input
if user_message := st.chat_input("Type your message here"):
    # Display user message in chat
    st.session_state["chat_history"].append({"role": "user", "text": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    # Get assistant response
    assistant_response = send_message_to_api(user_message, imageUrls)
    st.session_state["chat_history"].append({"role": "assistant", "text": assistant_response})

    # Display assistant response in chat
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
