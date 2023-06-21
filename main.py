import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read the dataset
df = pd.read_csv('heart_2020_cleaned.csv')

# Convert 'AgeCategory' column to numeric values
df['AgeCategory'] = pd.to_numeric(df['AgeCategory'], errors='coerce')

def main():
    st.title("Heart Disease Analysis")
    st.sidebar.title("Unique AgeCategory Categories")

    # Add a slider bar for age selection
    age_range = st.sidebar.slider("Select Age Range", 18, 80, (18, 80), step=1)

    # Filter the dataframe based on selected age range
    filtered_df = df[(df['AgeCategory'] >= age_range[0]) & (df['AgeCategory'] <= age_range[1])]

    # Plot the data
    fig = px.histogram(filtered_df, x='AgeCategory', y='HeartDisease', nbins=20, color='HeartDisease')
    fig.update_layout(
        title="Heart Disease Distribution by Age",
        xaxis_title="AgeCategory",
        yaxis_title="Amount of Heart Disease",
    )
    st.plotly_chart(fig)
<<<<<<< Updated upstream
    # st.write(df.head())
        
    # Group by 'Category' and calculate the sum of 'Value'
    df_copy = df[['AgeCategory',  'Sex', 'Race','HeartDisease']]
    grouped_df = df_copy.groupby(['AgeCategory',  'Sex', 'Race','HeartDisease' ]).size().reset_index(name='Count')
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


    # Select the relevant columns from the DataFrame
    diseases = ['SkinCancer', 'KidneyDisease', 'Asthma']
    
    df_copy1 = df.copy()
    df_copy1[['SkinCancer', 'KidneyDisease', 'Asthma']] = df_copy1[['SkinCancer', 'KidneyDisease', 'Asthma']].replace('Yes', 1)
    df_copy1[['SkinCancer', 'KidneyDisease', 'Asthma']] = df_copy1[['SkinCancer', 'KidneyDisease', 'Asthma']].replace('No', 0)
    
    # Create a new column for the combination of diseases
    df_copy1['DiseaseCombination'] = df_copy1[diseases].apply(lambda x: '_'.join(x.astype(str)), axis=1)
    
    # Define the custom labels for the disease combinations
    combination_labels = {
        '0_0_0': 'No Disease',
        '1_0_0': 'Skin Cancer',
        '0_1_0': 'Kidney Disease',
        '0_0_1': 'Asthma',
        '1_1_0': 'Skin Cancer, Kidney Disease',
        '1_0_1': 'Skin Cancer, Asthma',
        '0_1_1': 'Kidney Disease, Asthma',
        '1_1_1': 'Skin Cancer, Kidney Disease, Asthma'
    }
    
    dfHD = df_copy1.groupby(['HeartDisease', 'DiseaseCombination']).size().reset_index(name='Count')
    
    # Map the combination codes to the corresponding labels
    dfHD['CombinationLabel'] = dfHD['DiseaseCombination'].map(combination_labels)
    
    fig = px.bar(dfHD, x='Count', y='CombinationLabel', color='HeartDisease', barmode='stack', orientation='h')
    
    fig.update_layout(
        title='Combinations of Diseases by Heart Disease Grouping',
        xaxis=dict(title='Number of People'),
        yaxis=dict(title='Disease Combination'),
    )
    st.plotly_chart(fig)

    dfsleep = df_copy1.groupby(['HeartDisease', 'SleepTime']).size().reset_index(name='Count')
    print(dfsleep)
    
    fig = px.bar(dfsleep, x='Count', y='SleepTime', color='HeartDisease', barmode='stack', orientation='h')
    
    fig.update_layout(
        title='Sleep Time Distribution by Heart Disease Grouping',
        xaxis=dict(title='Number of People'),
        yaxis=dict(title='Sleep Time'),
    )
    
    st.plotly_chart(fig)
        

if __name__ == "__main__":
    main()
# C:\Users\ram63\Desktop\סמסטר ח\וויזואליזציה של מידע\PROJECT\GitHub\Visualization_Project2023
#streamlit run main.py
=======


if __name__ == "__main__":
    main()

#cd C:\Users\ram63\Desktop\סמסטר ח\וויזואליזציה של מידע\PROJECT\GitHub\Visualization_Project2023
#streamlit run main.py
>>>>>>> Stashed changes
