import streamlit as st

st.title("Streamlit minimal test")
st.write("If you see this, Streamlit is working.")
if st.button("Deploy"):
    st.write("Deploy button clicked")