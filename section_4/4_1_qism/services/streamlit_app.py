import streamlit as st
import requests

API_URL = "http://127.0.0.1:8080/generate_post"

st.title("LinkedIn Content Agent")
topic = st.text_input("Enter a topic for LinkedIn Post: ")

if st.button("Generate"):
    with st.spinner("Generating content..."):
        response = requests.post(API_URL, json={"topic": topic})
        data = response.json()

    if data.get("image_path"):
        st.image(data["image_path"], caption="Generated Thumbnail")
    else:
        st.warning("Image not generated")

    st.subheader("Generated content")
    st.write(data["post_text"])
