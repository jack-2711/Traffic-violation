import streamlit as st
import pandas as pd
import os

st.title("Smart Vehicle Violation Detection System")

if st.button("View Violation Log"):
    if os.path.exists("logs/violations.csv"):
        df = pd.read_csv("logs/violations.csv")
        st.dataframe(df)
    else:
        st.warning("No violations logged yet!")

if st.button("Show Snapshots"):
    st.write("Violation Images:")
    for img in os.listdir("violations"):
        st.image(os.path.join("violations", img), width=300)
