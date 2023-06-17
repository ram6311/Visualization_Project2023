# import streamlit as st
# import pandas as pd

# df = pd.read_csv('heart_data.csv')
# first_row = df.head(1)

# def main():
#     st.write("Hello, World!")
#     st.write(first_row)
    

# if __name__ == "__main__":
#     main()
!pip install matplotlib

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the dataset
df = pd.read_csv('heart_data.csv')

def main():
    st.title("Prevalence of Risk Factors for Heart Disease")
    
    # Sidebar filters
    selected_demo = st.sidebar.selectbox("Select Demographic Group", ["Age", "Sex", "Race"])
    
    # Filter and group the data based on the selected demographic group
    grouped_data = df.groupby(selected_demo)["target"].mean().reset_index()
    
    # Plotting
    plt.figure(figsize=(10, 6))
    sns.barplot(x=selected_demo, y="target", data=grouped_data)
    plt.xlabel(selected_demo)
    plt.ylabel("Prevalence of Heart Disease")
    plt.title(f"Comparison of Heart Disease Prevalence by {selected_demo}")
    st.pyplot()
    
if __name__ == "__main__":
    main()

