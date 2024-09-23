import sys
import os

# Adjust the path to locate your app package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from app.main import app  # Adjust as needed
import streamlit as st

# Simple Streamlit interface
st.title("My FastAPI with Streamlit")
st.write("This is a placeholder for your app.")
