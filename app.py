import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import networkx as nx

st.title("CSV Data Visualization")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("DataFrame:")
    st.write(df)

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    st.write("Summary Statistics:")
    st.write(df.describe())

    st.write("Visualizations:")

    # Interactive Line Chart for tracking changes over time
    if 'date' in df.columns:
        fig = px.line(df, x='date', y='amount', color='type', title='Income and Expenses Over Time')
        fig.update_layout(height=600, width=1000)
        st.plotly_chart(fig)

    # Bar Chart with Filters
    category_filter = st.multiselect('Filter by category', options=df['category'].unique(), default=df['category'].unique())
    filtered_df = df[df['category'].isin(category_filter)]
    fig = px.bar(filtered_df, x='category', y='amount', color='type', barmode='group', title='Amount by Category')
    fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig)

    # Interactive Pie Chart for income vs expenses
    fig = px.pie(df, names='type', values='amount', title='Income vs Expenses')
    fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig)

    # Treemap for hierarchical data
    fig = px.treemap(df, path=['type', 'category'], values='amount', title='Treemap of Expenses and Income')
    fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig)

    # Interactive Histogram
    fig = px.histogram(df, x='amount', nbins=10, title='Distribution of Amounts', marginal='rug')
    fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig)

    # Sankey Diagram
    if 'category' in df.columns:
        income_df = df[df['type'] == 'income']
        expense_df = df[df['type'] == 'expense']
        
        labels = ['Income'] + expense_df['category'].unique().tolist()
        sources = [0] * len(expense_df)
        targets = [labels.index(category) for category in expense_df['category']]
        values = expense_df['amount']

        sankey_fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
                color="blue"
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values
            )
        )])

        sankey_fig.update_layout(title_text="Flow of Money from Income to Expense Categories", font_size=10, height=600, width=1000)
        st.plotly_chart(sankey_fig)

    # Interactive Bubble Chart
    fig = px.scatter(df, x='date', y='amount', size='amount', color='type', hover_name='description', title='Bubble Chart of Amounts Over Time')
    fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig)

    # Box Plot
    st.write("Box Plot of Amounts by Type:")
    fig = px.box(df, x='type', y='amount', points="all", title='Box Plot of Amounts by Type')
    fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig)

    # Violin Plot
    st.write("Violin Plot of Amounts by Type:")
    fig = px.violin(df, x='type', y='amount', box=True, points="all", title='Violin Plot of Amounts by Type')
    fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig)

    # Heatmap
    st.write("Heatmap of Amounts:")
    heatmap_data = df.pivot_table(index='category', columns='type', values='amount', aggfunc='sum')
    fig = px.imshow(heatmap_data, text_auto=True, aspect="auto", title='Heatmap of Amounts by Category and Type')
    fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig)

    # Sunburst Chart
    st.write("Sunburst Chart:")
    fig = px.sunburst(df, path=['type', 'category'], values='amount', title='Sunburst Chart of Amounts')
    fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig)

    # Scatter Matrix
    st.write("Scatter Matrix:")
    fig = px.scatter_matrix(df, dimensions=['amount'], color='type', title='Scatter Matrix of Amounts')
    fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig)

    # 3D Scatter Plot
    if 'date' in df.columns:
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        fig = px.scatter_3d(df, x='year', y='month', z='amount', color='type', title='3D Scatter Plot of Amounts Over Time')
        fig.update_layout(height=600, width=1000)
        st.plotly_chart(fig)

    # Word Cloud
    if 'description' in df.columns:
        st.write("Word Cloud of Descriptions:")
        text = ' '.join(df['description'].astype(str).tolist())
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

    # Parallel Coordinates Plot
    st.write("Parallel Coordinates Plot:")
    fig = px.parallel_coordinates(df, color='amount', labels={"amount": "Amount", "type": "Type", "category": "Category"},
                                  title='Parallel Coordinates Plot')
    fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig)

    # Radial Bar Chart
    st.write("Radial Bar Chart:")
    fig = px.bar_polar(df, r='amount', theta='category', color='type', title='Radial Bar Chart of Amounts by Category')
    fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig)

    # Offer download link for the processed data
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='downloaded_file.csv',
        mime='text/csv',
    )

else:
    st.write("Please upload a CSV file.")