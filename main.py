import streamlit as st
import pandas as pd

df = pd.read_csv('heart_data.csv')
first_row = df.head(1)

def main():
    st.write("Hello, World!")
    st.write(first_row)
    

if __name__ == "__main__":
    main()
