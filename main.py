import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

    # Plotting the data
    fig, ax = plt.subplots(2, 2, figsize=(12, 8))

    # Customize and plot the subplots
    # Note: You will need to adjust the specific plot type and customization based on your data and visualization requirements

    # Subplot 1
    ax[0, 0].bar(filtered_data["Race"], filtered_data["Variable1"])
    ax[0, 0].set_title("Plot 1")

    # Subplot 2
    ax[0, 1].scatter(filtered_data["Race"], filtered_data["Variable2"])
    ax[0, 1].set_title("Plot 2")

    # Subplot 3
    ax[1, 0].plot(filtered_data["Race"], filtered_data["Variable3"])
    ax[1, 0].set_title("Plot 3")

    # Subplot 4
    ax[1, 1].pie(filtered_data["Variable4"], labels=filtered_data["Race"])
    ax[1, 1].set_title("Plot 4")

    # Display the plot in Streamlit
    st.pyplot(fig)


if __name__ == "__main__":
    main()


