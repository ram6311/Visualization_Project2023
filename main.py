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
    # st.write(df.head())
        
    # Group by 'Category' and calculate the sum of 'Value'
    grouped_df = df.groupby(['AgeCategory',  'Sex', 'Race','HeartDisease' ]).sum()
    
    print(grouped_df)
    

if __name__ == "__main__":
    main()
# C:\Users\ram63\Desktop\סמסטר ח\וויזואליזציה של מידע\PROJECT\GitHub\Visualization_Project2023
#streamlit run main.py
