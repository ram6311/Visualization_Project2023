import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    
    fig = go.Figure()
    
    fig.update_layout(
        template="simple_white",
        xaxis=dict(title_text="AgeCategory"),
        yaxis=dict(title_text="Count"),
        barmode="group",
    )
    
    colors = ["#2A66DE", "#FFC32B", "#FF5733", "#8B008B", "#00FF00", "#FFD700"]
    
    # Filter the DataFrame for female with heart disease
    female_hd_df = grouped_df[(grouped_df['Sex'] == 'Female') & (grouped_df['HeartDisease'] == 'Yes')]
    fig.add_trace(
        go.Bar(x=female_hd_df['AgeCategory'], y=female_hd_df['Count'], name='Female with Heart Disease', marker_color=colors[0])
    )
    
    # Filter the DataFrame for female without heart disease
    female_no_hd_df = grouped_df[(grouped_df['Sex'] == 'Female') & (grouped_df['HeartDisease'] == 'No')]
    fig.add_trace(
        go.Bar(x=female_no_hd_df['AgeCategory'], y=female_no_hd_df['Count'], name='Female without Heart Disease', marker_color=colors[1])
    )
    
    # Filter the DataFrame for male with heart disease
    male_hd_df = grouped_df[(grouped_df['Sex'] == 'Male') & (grouped_df['HeartDisease'] == 'Yes')]
    fig.add_trace(
        go.Bar(x=male_hd_df['AgeCategory'], y=male_hd_df['Count'], name='Male with Heart Disease', marker_color=colors[2])
    )
    
    # Filter the DataFrame for male without heart disease
    male_no_hd_df = grouped_df[(grouped_df['Sex'] == 'Male') & (grouped_df['HeartDisease'] == 'No')]
    fig.add_trace(
        go.Bar(x=male_no_hd_df['AgeCategory'], y=male_no_hd_df['Count'], name='Male without Heart Disease', marker_color=colors[3])
    )
    
    
    st.plotly_chart(fig)


    

if __name__ == "__main__":
    main()
# C:\Users\ram63\Desktop\סמסטר ח\וויזואליזציה של מידע\PROJECT\GitHub\Visualization_Project2023
#streamlit run main.py
