import streamlit as st
import pandas as pd
import plotly.express as px

# Read the dataset
df = pd.read_csv('heart_2020_cleaned.csv')

def main():
    # Create the Streamlit app
    st.title("Interactive Plot")
    
    # Select the variable for x-axis
    x_variable = st.selectbox("Select X variable:", df.columns)

    # Plotting the data using Plotly Express
    fig = px.histogram(df, x=x_variable)
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
