import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import seaborn as sns
import plotly.figure_factory as ff
import numpy as np



# Read the dataset
df = pd.read_csv('heart_2020_cleaned.csv')
#change the columns from AgeCategory to Age
df['Age'] = df['AgeCategory']
df = df.drop(columns=['AgeCategory'])


def main():
    # Set page title
    # Title and Description
    _, col, _ = st.columns((0.6, 3, 0.1))
    with col:
        st.title('Heart Disease Dashboard')
    _, col, _ = st.columns((0.2, 3, 0.1))
    with col:
        st.subheader('Visualization Project by Adar Harari and Ram Manor')
    _, col, _ = st.columns((2.1, 3, 0.1))
    with col:
        st.markdown("[GitHub Repository](https://github.com/ram6311/Visualization_Project2023)")

    _, col, _ = st.columns((1.7, 3, 1.8))
    with col:
        st.markdown(
            "<p style='text-align: center;'>This <em>Streamlit</em> app serves as a dashboard for analyzing heart disease data. The dataset contains information about people with heart disease, and the app provides various visualizations to explore the data and gain insights.</p>",
            unsafe_allow_html=True
        )

    if 'selected_ages' not in st.session_state:
        sorted_list = sorted(df['Age'].unique().tolist())
        st.session_state.selected_ages = sorted_list

    # Add a multiselect widget for selected ages
    selected_ages = st.multiselect('Selected Age', df['Age'].unique(), default=st.session_state.selected_ages)

    # Update session state with selected ages
    st.session_state.selected_ages = selected_ages

    # Filter data
    filtered_df = df[df['Age'].isin(selected_ages)]

    # Mode selection between Heart Disease with Yes or No
    mode_Heart = st.sidebar.radio("Switch Heart Disease", ["Heart Disease All", "No","Yes" ], index=0)

    if mode_Heart == "Heart Disease All":
        filtered_df = filtered_df
    else:
        filtered_df = filtered_df[filtered_df['HeartDisease'] == mode_Heart]

    # Add a radio button group for selecting sex
    sex_options = ['All Genders', 'Male', 'Female']
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
    try: # if the user didn't select any age, the graph will not be shown
        # Group by Age and count number of people with heart disease
        age_counts = filtered_df.groupby('Age').size().reset_index(name='Count')

        # Create subplot grid with 1 row and 2 columns
        fig = make_subplots(rows=1, cols=2, subplot_titles=["Bar Chart", "Line Chart"])

        # Bar plot for number of people with heart disease
        fig.add_trace(go.Bar(x=age_counts['Age'], y=age_counts['Count'], marker_color=marker_color_sex), row=1, col=1)
        mode_Heart2 = mode_Heart
        if mode_Heart2 == "Heart Disease All":
            mode_Heart2 = "Yes"
        # Line plot for heart disease percentage
        heart_disease_percentage = filtered_df.groupby('Age')['HeartDisease'].apply(
            lambda x: (x == mode_Heart2).mean()).reset_index(name='Percentage')
        fig.add_trace(
            go.Scatter(x=heart_disease_percentage['Age'], y=heart_disease_percentage['Percentage'],
                       marker_color=marker_color_sex), row=1,
            col=2)

        fig.update_layout(
            title=f'Age Distribution and Heart Disease Prevalence',
            height=400,

            showlegend=False
        )

        fig.update_xaxes(title_text="Age", row=1, col=1)
        fig.update_xaxes(title_text="Age", row=1, col=2)
        fig.update_yaxes(title_text="Number of People", row=1, col=1)
        fig.update_yaxes(title_text="Percentage", row=1, col=2)

        # # Display subplot grid
        st.write(f" Data set to : {mode_Heart} & {selected_sex}")
        st.plotly_chart(fig)

        ##### Graph 2 #####
        # Group by 'Category' and calculate the sum of 'Value'
        df_copy = filtered_df[['Age', 'Sex', 'Race', 'HeartDisease']]
        grouped_df = df_copy.groupby(['Age', 'Sex', 'Race', 'HeartDisease']).size().reset_index(name='Count')
        fig = go.Figure()



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
        fig.update_layout(
            title=f'Impact of Demographic Factors on Heart Disease Risk',
            height=400,

            showlegend=True,
            annotations=[
                dict(
                    text=f" Data set to : {mode_Heart} & {selected_sex}",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0,
                    y=1.1,
                    align="center",
                    font=dict(size=15)
                )
            ]
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
        if mode_Heart == "Yes" and selected_sex == "All Genders":
            st.plotly_chart(fig)
        else:
            st.write(title_text="Percentage of people with heart disease for each Gender")

            st.write("Please select 'Yes' on Switch Heart Disease and 'All Genders' on Selected Sex to display the plot.")

        ##### Graph 4 #####
        # List of diseases
        diseases = ['Stroke', 'Diabetic', 'Asthma', 'KidneyDisease', 'SkinCancer']

        # Count the occurrences of "Yes" and "No" for each disease
        counts = filtered_df[diseases].apply(lambda x: x.value_counts()).T

        # Create a stacked bar plot using Plotly
        fig = go.Figure(data=[
            go.Bar(name='Yes', x=counts.index, y=counts['Yes'], marker_color=marker_color_sex),
            go.Bar(name='No', x=counts.index, y=counts['No'])
        ])



        fig.update_layout(
            xaxis_title='Disease',
            yaxis_title='Count',
            barmode='stack',
            title=f'The prevalence of diseases among the population',
            height=400,

            showlegend=True,
            annotations=[
                dict(
                    text=f" Data set to : {mode_Heart} & {selected_sex}",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0,
                    y=1.1,
                    align="center",
                    font=dict(size=15)
                )
            ]
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

        fig.update_layout(
            title=f'Percentage of Sleep Times by Heart Disease',
            height=400,

            showlegend=True,
            annotations=[
                dict(
                    text=f" Data set to : {mode_Heart} & {selected_sex}",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0,
                    y=1.1,
                    align="center",
                    font=dict(size=15)
                )
            ]
        )
        # Display the plot using Streamlit
        st.plotly_chart(fig)



        _, col, _ = st.columns((0.04, 3, 0.1))
        with col:
            st.subheader('Impact of Lifestyle Factors  on Heart Disease Risk')
        ##### Graph 6 #####
        colors2 = ['#1337f5', '#E80000']

        x = filtered_df.groupby('HeartDisease').PhysicalActivity.value_counts().reset_index(name='Count').Count

        fig = px.pie(names=['Physical Activity', 'No physical activity'], values=[x[0], x[1]],
                     color_discrete_sequence=colors2)

        fig.update_layout(
            title=f'In reference to physical activity',
            height=400,

            showlegend=True,
            annotations=[
                dict(
                    text=f" Data set to : {mode_Heart} & {selected_sex}",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0,
                    y=1.1,
                    align="center",
                    font=dict(size=15)
                )
            ]
        )

        if mode_Heart != "Heart Disease All":
            st.plotly_chart(fig)
        else:
            st.write(
                title_text="Percentage of Individuals Reporting Physical Activities in The Past 30 Days - Individuals with or Without Heart Disease")

            st.write("Please select 'Yes' or 'No' on Switch Heart Disease to display the plot.")

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
                    perc = filtered_df.groupby(col)[according_to].value_counts(normalize=True).reset_index(
                        name='Percentage')
                    fig = px.bar(perc, x=col, y='Percentage', color=according_to, barmode='group',
                                 color_discrete_map={'Yes': '#E80000', 'No': '#1337f5'},
                                 category_orders={col: filtered_df[col].value_counts().index})
                else:
                    fig = px.histogram(filtered_df, x=col, color=according_to, color_discrete_sequence=colors1,
                                       category_orders={col: filtered_df[col].value_counts().index})

            if according_to is None:
                fig.update_layout(title=f'{col}')
            else:
                column=''
                if col == 'Smoking':
                    column='Smoking'
                elif col == 'AlcoholDrinking':
                    column='Alcohol Consumption'
                elif col == 'DiffWalking':
                    column='Walking difficulties'
                fig.update_layout(
                    title=f'{column} ',
                    height=400,

                    showlegend=True,
                    annotations=[
                        dict(
                            text=f" Data set to : {mode_Heart} & {selected_sex}",
                            showarrow=False,
                            xref="paper",
                            yref="paper",
                            x=0,
                            y=1.1,
                            align="center",
                            font=dict(size=15)
                        )
                    ]
                )

            if mode_Heart == "Heart Disease All":
                st.plotly_chart(fig)
            else:
                if according_to is None:
                    st.write(title=f'{col}')
                else:
                    st.write(title=f'{col} according to {according_to}')
                st.write("Please select 'Heart Disease All' on Switch Heart Disease to display the plot.")

        # Call the function
        show_relation(obj_cols[0], 'HeartDisease', type_='count')
        show_relation(obj_cols[1], 'HeartDisease', type_='count')
        show_relation(obj_cols[3], 'HeartDisease', type_='count')

        ##### Graph 8 #####

       # Display the plot using Streamlit
        try:
            # Create a new column called BMI Category
            x1 = filtered_df[filtered_df['HeartDisease'] == 'Yes']['BMI']
            x2 = filtered_df[filtered_df['HeartDisease'] == 'No']['BMI']

            # Downsample the data or aggregate it if needed
            # Example of downsampling:
            downsampled_x1 = np.random.choice(x1, size=1000, replace=False)
            downsampled_x2 = np.random.choice(x2, size=1000, replace=False)

            # Compute the KDE for the downsampled data
            kde_x1 = np.random.normal(loc=downsampled_x1.mean(), scale=downsampled_x1.std(), size=10000)
            kde_x2 = np.random.normal(loc=downsampled_x2.mean(), scale=downsampled_x2.std(), size=10000)

            hist_data = [kde_x1, kde_x2]
            group_labels = ['HeartDisease', 'NoHeartDisease']
            colors = ['#1337f5', '#E80000']

            # Create distplot with precomputed distributions
            fig = ff.create_distplot(hist_data, group_labels, show_hist=False, colors=colors)

            # Update layout and axis labels
            fig.update_layout(title='BMI Distribution', xaxis_title='BMI', yaxis_title='Density',

                height=400,

                showlegend=True,
                annotations=[
                    dict(
                        text=f" Data set to : {mode_Heart} & {selected_sex}",
                        showarrow=False,
                        xref="paper",
                        yref="paper",
                        x=0,
                        y=1.1,
                        align="center",
                        font=dict(size=15)
                    )
                ]
            )
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.write("Please select 'Heart Disease All' on Switch Heart Disease to display the plot.")
    except:
        _, col, _ = st.columns((0.04, 3, 0.1))
        with col:
            st.subheader('No data to display. Please select at least one age group.')
if __name__ == "__main__":
    main()
