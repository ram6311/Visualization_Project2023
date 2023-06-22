import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import seaborn as sns
import plotly.figure_factory as ff



# Read the dataset
df = pd.read_csv('heart_2020_cleaned.csv')
columns = ['HeartDisease', 'BMI', 'Smoking', 'AlcoholDrinking', 'Stroke',
       'PhysicalHealth', 'MentalHealth', 'DiffWalking', 'Sex', 'Age', 'Race',
       'Diabetic', 'PhysicalActivity', 'GenHealth', 'SleepTime', 'Asthma',
       'KidneyDisease', 'SkinCancer']
#change the columns from AgeCategory to Age
df['Age'] = df['AgeCategory']
df = df.drop(columns=['AgeCategory'])


def main():
    st.title('Heart Disease Dashboard')

    if 'selected_ages' not in st.session_state:
        sorted_list= sorted(df['Age'].unique().tolist())
        st.session_state.selected_ages = sorted_list

    # Add a multiselect widget for selected ages
    selected_ages = st.multiselect('Selected Age', df['Age'].unique(), default=st.session_state.selected_ages)

    # Update session state with selected ages
    st.session_state.selected_ages = selected_ages

    # Calculate remaining age ranges
    remaining_ages = [age for age in df['Age'].unique() if age not in selected_ages]

    # Add a multiselect widget for remaining age ranges
    rem_ages = st.multiselect('Remaining Age Ranges', df['Age'].unique(), default=remaining_ages)

    # Update session state with remaining age ranges
    st.session_state.rem_ages = rem_ages

    # Filter data

    # Mode selection between selected and remaining age ranges
    mode_age = st.sidebar.radio("Switch Selected Ages", ("Selected Ages", "Remaining Ages"))

    # Filter data based on mode selection
    if mode_age == "Selected Ages":
        filtered_df = df[df['Age'].isin(selected_ages)]
    else:
        filtered_df = df[df['Age'].isin(rem_ages)]

    # Mode selection between Heart Disease with Yes or No
    mode_Heart = st.sidebar.radio("Switch Heart Disease", ["Yes", "No", "Heart Disease All"], index=0)
    if mode_Heart == "Heart Disease All":
        filtered_df = filtered_df
    else:
        filtered_df = df[df['HeartDisease'] == mode_Heart]


    # Add a radio button group for selecting sex
    sex_options = ['All Genders','Male', 'Female' ]
    selected_sex = st.sidebar.radio('Selected Sex', sex_options, index=0)
    marker_color_sex = 'red'
    # Update filtered_df with selected sex
    if selected_sex == 'All Genders':
        filtered_df = filtered_df
        marker_color_sex = 'red'
    else:
        filtered_df = filtered_df[filtered_df['Sex'] == selected_sex]
        if selected_sex == 'Male':
            marker_color_sex = 'blue'
        else:
            marker_color_sex = 'pink'

    # Group by Age and count number of people with heart disease
    age_counts = filtered_df[filtered_df['HeartDisease'] == 'Yes'].groupby('Age').size().reset_index(name='Count')

    # Create subplot grid with 1 row and 2 columns
    fig = make_subplots(rows=1, cols=2, subplot_titles=["Bar Chart", "Line Chart"])

    # Bar plot for number of people with heart disease
    fig.add_trace(go.Bar(x=age_counts['Age'], y=age_counts['Count'], marker_color=marker_color_sex), row=1, col=1)

    # Line plot for heart disease percentage
    heart_disease_percentage = filtered_df.groupby('Age')['HeartDisease'].apply(
        lambda x: (x == 'Yes').mean()).reset_index(name='Percentage')
    fig.add_trace(
        go.Scatter(x=heart_disease_percentage['Age'], y=heart_disease_percentage['Percentage'], marker_color=marker_color_sex), row=1,
        col=2)

    # Update layout and axis labels
    fig.update_layout(title=f'Heart Disease Analysis ({mode_age})', height=400, showlegend=False)
    fig.update_xaxes(title_text="Age", row=1, col=1)
    fig.update_xaxes(title_text="Age", row=1, col=2)
    fig.update_yaxes(title_text="Number of People", row=1, col=1)
    fig.update_yaxes(title_text="Percentage", row=1, col=2)

    # # Display subplot grid
    st.plotly_chart(fig)
                                                        ##### Graph 2 #####
    # Group by 'Category' and calculate the sum of 'Value'
    df_copy = filtered_df[['Age', 'Sex', 'Race', 'HeartDisease']]
    grouped_df = df_copy.groupby(['Age', 'Sex', 'Race', 'HeartDisease']).size().reset_index(name='Count')
    fig = go.Figure()

    fig.update_layout(
        template="simple_white",
        xaxis=dict(title_text="Age"),
        yaxis=dict(title_text="Count"),
        barmode="group",
    )

    colors = ["#2A66DE", "#FFC32B", "#FF5733", "#8B008B", "#00FF00", "#FFD700"]

    # Filter the DataFrame for female with heart disease
    female_hd_df = grouped_df[(grouped_df['Sex'] == 'Female') & (grouped_df['HeartDisease'] == 'Yes')]
    fig.add_trace(
        go.Bar(x=female_hd_df['Age'], y=female_hd_df['Count'], name='Female with Heart Disease',
               marker_color=colors[0])
    )

    # Filter the DataFrame for female without heart disease
    female_no_hd_df = grouped_df[(grouped_df['Sex'] == 'Female') & (grouped_df['HeartDisease'] == 'No')]
    fig.add_trace(
        go.Bar(x=female_no_hd_df['Age'], y=female_no_hd_df['Count'], name='Female without Heart Disease',
               marker_color=colors[1])
    )

    # Filter the DataFrame for male with heart disease
    male_hd_df = grouped_df[(grouped_df['Sex'] == 'Male') & (grouped_df['HeartDisease'] == 'Yes')]
    fig.add_trace(
        go.Bar(x=male_hd_df['Age'], y=male_hd_df['Count'], name='Male with Heart Disease',
               marker_color=colors[2])
    )

    # Filter the DataFrame for male without heart disease
    male_no_hd_df = grouped_df[(grouped_df['Sex'] == 'Male') & (grouped_df['HeartDisease'] == 'No')]
    fig.add_trace(
        go.Bar(x=male_no_hd_df['Age'], y=male_no_hd_df['Count'], name='Male without Heart Disease',
               marker_color=colors[3])
    )

    st.plotly_chart(fig)

                                                        ##### Graph 3 #####

    df_plot = filtered_df[filtered_df['HeartDisease'] == 'Yes']
    fig = px.pie(
        values=df_plot['Sex'].value_counts().values,
        names=df_plot['Sex'].value_counts().index,
        color=df_plot['Sex'].value_counts().index,
        color_discrete_map={'Male': 'blue', 'Female': 'pink'}
    )
    fig.update_traces(textposition='inside', textinfo='percent+label', pull=[0.05, 0])
    fig.update_layout(legend_title="Labels", font=dict(size=20))
    fig.update_layout(title_text="Percentage of people with heart disease for each Gender")

    st.plotly_chart(fig)
                            ##### Graph 4 #####
    # List of diseases
    diseases = ['Stroke', 'Diabetic', 'Asthma', 'KidneyDisease', 'SkinCancer']

    # Count the occurrences of "Yes" and "No" for each disease
    counts = filtered_df[diseases].apply(lambda x: x.value_counts()).T

    # Create a stacked bar plot using Plotly
    fig = go.Figure(data=[
        go.Bar(name='Yes', x=counts.index, y=counts['Yes']),
        go.Bar(name='No', x=counts.index, y=counts['No'])
    ])

    # Update layout and axis labels
    fig.update_layout(
        title='Count of Yes and No for Each Disease',
        xaxis_title='Disease',
        yaxis_title='Count',
        barmode='stack'
    )

    # Display the plot using Streamlit
    st.plotly_chart(fig, use_container_width=True)

                            ##### Graph 5 #####
    # Group by HeartDisease and SleepTime and calculate the count
    relative = filtered_df.groupby('HeartDisease').SleepTime.value_counts(normalize=True).reset_index(name='Percentage')


    # Define the colors for the bar chart
    colors = ['#1337f5', '#E80000']

    # Create the bar chart
    fig = px.bar(relative, x='SleepTime', y='Percentage', color='HeartDisease', barmode='group',
                 color_discrete_sequence=colors)

    # Update layout and title
    fig.update_layout(title="Percentage of Sleep Times by Heart Disease")

    # Display the plot using Streamlit
    st.plotly_chart(fig)
        ##### Graph 6 #####
    colors2 = ['#1337f5', '#E80000']

    x = filtered_df.groupby('HeartDisease').PhysicalActivity.value_counts().reset_index(name='Count').Count

    fig = px.pie(names=['Physical Activity', 'No physical activity'], values=[x[0], x[1]],
                 color_discrete_sequence=colors2)
    fig.update_layout(
        title="Percentage of Individuals Reporting Physical Activities in The Past 30 Days - Individuals with or Without Heart Disease")
    st.plotly_chart(fig)

    ##### Graph 7 #####

    colors6 = sns.color_palette(['#1337f5', '#E80000', '#0f1e41', '#fd523e', '#404e5c', '#c9bbaa'], 6)
    colors2 = sns.color_palette(['#1337f5', '#E80000'], 2)
    colors1 = sns.color_palette(['#1337f5'], 1)
    obj_cols = filtered_df.select_dtypes(include='object').columns[1:]

    def show_relation(col, according_to, type_='dis'):
        if type_ == 'dis':
            fig = px.histogram(filtered_df, x=col, color=according_to, marginal='kde', color_discrete_sequence=colors2)
        elif type_ == 'count':
            if according_to is not None:
                perc = filtered_df.groupby(col)[according_to].value_counts(normalize=True).reset_index(name='Percentage')
                fig = px.bar(perc, x=col, y='Percentage', color=according_to, barmode='group',
                             color_discrete_map={0: colors2[0], 1: colors2[1]},
                             category_orders={col: filtered_df[col].value_counts().index})
            else:
                fig = px.histogram(filtered_df, x=col, color=according_to, color_discrete_sequence=colors1,
                                   category_orders={col: filtered_df[col].value_counts().index})

        if according_to is None:
            fig.update_layout(title=f'{col}')
        else:
            fig.update_layout(title=f'{col} according to {according_to}')

        if mode_Heart != "Heart Disease All":
            st.plotly_chart(fig)
        else:
            st.write("Please select a specific mode to display the plot.")

           
        #st.plotly_chart(fig)

    # Call the function
    show_relation(obj_cols[0], 'HeartDisease', type_='count')
    show_relation(obj_cols[1], 'HeartDisease', type_='count')
    show_relation(obj_cols[3], 'HeartDisease', type_='count')


    # x1 = filtered_df[filtered_df['HeartDisease']=='Yes']['BMI']
    # x2 = filtered_df[filtered_df['HeartDisease']=='No']['BMI']

    # hist_data = [x1, x2]

    # group_labels = ['HeartDisease', 'NoHeartDisease']
    # colors = ['#1337f5', '#E80000']

    # fig = ff.create_distplot(hist_data, group_labels, show_hist=False, colors=colors)

    # fig.update_xaxes(title_text='BMI')
    # fig.update_yaxes(title_text='Density')

    # fig.update_layout(title_text='BMI distribution')
    # st.plotly_chart(fig)

if __name__ == "__main__":
    main()

#cd C:\Users\ram63\Desktop\סמסטר ח\וויזואליזציה של מידע\PROJECT\GitHub\Visualization_Project2023
#streamlit run main.py
