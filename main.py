import streamlit as st
import pandas as pd
import plotly.express as px

# Read the dataset
df = pd.read_csv('heart_2020_cleaned.csv')

def main():
    # Define unique values for AgeCategory, Race, Sex, and HeartDisease
    age_categories = df["AgeCategory"].unique()
    races = df["Race"].unique()
    sexes = df["Sex"].unique()
    heart_diseases = df["HeartDisease"].unique()

    # Create the Streamlit app
    st.title("Interactive Plot")
    selected_age_category = st.selectbox("Select Age Category:", age_categories)
    selected_race = st.selectbox("Select Race:", races)
    selected_sex = st.selectbox("Select Sex:", sexes)
    selected_heart_disease = st.selectbox("Select Heart Disease:", heart_diseases)

    # Filter the data based on user selections
    filtered_data = df[
        (df["AgeCategory"] == selected_age_category)
        & (df["Race"] == selected_race)
        & (df["Sex"] == selected_sex)
        & (df["HeartDisease"] == selected_heart_disease)
    ]

    # Plotting the data using Plotly Express
    fig = px.bar(filtered_data, x="Race", y="Variable1", title="Plot 1")
    st.plotly_chart(fig)

    fig = px.scatter(filtered_data, x="Race", y="Variable2", title="Plot 2")
    st.plotly_chart(fig)

    fig = px.line(filtered_data, x="Race", y="Variable3", title="Plot 3")
    st.plotly_chart(fig)

    fig = px.pie(filtered_data, names="Race", values="Variable4", title="Plot 4")
    st.plotly_chart(fig)


if __name__ == "__main__":
    main()
