import streamlit as st

st.write(
    """
# Apps with widgets!
"""
)
x = st.slider("Select a number", 0, 100)
st.write("You selected", x)
