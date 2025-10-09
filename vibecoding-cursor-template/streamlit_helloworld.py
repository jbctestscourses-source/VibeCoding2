##pip install streamlit

import streamlit as st
import requests

# Set the title and icon for the browser tab
st.set_page_config(
    page_title="Random Kitten Viewer 🐾",
    page_icon="🐱"
)

# --- Function to fetch a random kitten image ---
def get_random_kitten_image():
    try:
        # TheCatAPI provides random cat images.
        # We can specify 'mime_types' to ensure we get images.
        response = requests.get("https://api.thecatapi.com/v1/images/search?mime_types=jpg,png,gif")
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data:
            return data[0]['url']
        else:
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching kitten image: {e}")
        return None

# --- Streamlit App Layout ---

st.title("Adorable Kitten Generator! 😻")
st.write("Click the button below to see a new furry friend!")

# Use a session state to store the current image URL
# This prevents the image from changing on every rerun unless the button is pressed
if 'kitten_url' not in st.session_state:
    st.session_state.kitten_url = get_random_kitten_image()

# Button to get a new kitten
if st.button("Get New Kitten 🐾"):
    st.session_state.kitten_url = get_random_kitten_image()

# Display the kitten image if available
if st.session_state.kitten_url:
    st.image(st.session_state.kitten_url, caption="Here's a cute kitten!", use_column_width=True)
else:
    st.info("Couldn't fetch a kitten image. Please try again later.")

st.markdown("---")
st.write("Powered by [TheCatAPI](https://thecatapi.com/)")