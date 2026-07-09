import os
import streamlit as st


def get_secret(name: str):

    # Streamlit Cloud
    if name in st.secrets:
        return st.secrets[name]

    # Local development
    return os.getenv(name)