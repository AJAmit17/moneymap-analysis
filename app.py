import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the title
st.title("CSV Data Visualization")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display the DataFrame
    st.write("DataFrame:")
    st.write(df)
    
    # Convert date column to datetime if it exists
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # Visualizations
    st.write("Visualizations:")
    
    # Plot total income and expenses
    fig, ax = plt.subplots()
    sns.barplot(x='type', y='amount', data=df, estimator=sum, ax=ax)
    ax.set_title('Total Income and Expenses')
    st.pyplot(fig)
    
    # Plot expenses by category
    expense_df = df[df['type'] == 'expense']
    fig, ax = plt.subplots()
    sns.barplot(x='category', y='amount', data=expense_df, estimator=sum, ax=ax)
    ax.set_title('Expenses by Category')
    st.pyplot(fig)
    
    # Plot income and expenses over time if date column exists
    if 'date' in df.columns:
        fig, ax = plt.subplots()
        sns.lineplot(x='date', y='amount', hue='type', data=df, ax=ax)
        ax.set_title('Income and Expenses Over Time')
        st.pyplot(fig)
else:
    st.write("Please upload a CSV file.")