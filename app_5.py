import pandas as pd
import plotly.express as px
import streamlit as st

# Streamlit app
st.title("Dynamic Ticket Visualization")
st.write("This app visualizes hierarchical data with counts and percentages.")

# Option to toggle between local data and file upload
use_local_data = st.sidebar.checkbox("Use Local Data", value=True)

if use_local_data:
    # Load local data
    st.info("Using local data for the visualization.")
    # Replace this with your local dataset
    df = pd.read_csv('C:\\others\\Code\\VSCode\\data-vis-webapp\\ZD_Themes_and_SubThemes.csv')
else:
    # File uploader
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Please upload a CSV file or enable local data.")
        st.stop()

# Sidebar panel for column selection
st.sidebar.title("Column Selection")

# Column selection for themes and sub-themes with "None" as an option
theme_column = st.sidebar.selectbox(
    "Select the first column (Theme):",
    options=["None"] + list(df.columns),
    index=0
)

sub_theme_column = st.sidebar.selectbox(
    "Select the second column (Sub-Theme):",
    options=["None"] + list(df.columns),
    index=0
)

channel_column = st.sidebar.selectbox(
    "Select the column for Channels or Additional Breakdown:",
    options=["None"] + list(df.columns),
    index=0
)

# Fill NaN or remove invalid rows
if theme_column != "None":
    df[theme_column] = df[theme_column].fillna("Unknown Theme")
if sub_theme_column != "None":
    df[sub_theme_column] = df[sub_theme_column].fillna("Unknown Sub-Theme")
if channel_column != "None":
    df[channel_column] = df[channel_column].fillna("Unknown Channel")

# User input for dynamic filtering
st.sidebar.subheader("Optional Filters")
if theme_column != "None":
    selected_theme = st.sidebar.selectbox(
        "Filter by Theme (Optional):",
        options=["All"] + list(df[theme_column].unique())
    )
    if selected_theme != "All":
        df = df[df[theme_column] == selected_theme]

# Prepare the hierarchy path based on selected columns
hierarchy_path = []
if theme_column != "None":
    hierarchy_path.append(theme_column)
if sub_theme_column != "None":
    hierarchy_path.append(sub_theme_column)
if channel_column != "None":
    hierarchy_path.append(channel_column)

# Check if hierarchy_path is empty before grouping
if hierarchy_path:
    # Calculate count for each combination of hierarchical columns
    df_counts = df.groupby(hierarchy_path).size().reset_index(name='count')

    # Calculate percentage for each combination
    total_count = df_counts['count'].sum()
    df_counts['percentage'] = (df_counts['count'] / total_count) * 100

    # Create Sunburst plot if hierarchy columns are selected
    fig = px.sunburst(
        df_counts,
        path=hierarchy_path,
        values='count',  # Use count for the size of the segments
        title="Hierarchical Visualization of Data with Percentages",
        labels={col: col for col in hierarchy_path},
    )

    # Add the count and percentage as customdata for every level
    fig.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"  # Label
            + "Count: %{customdata[0]}<br>"  # Count value
            + "Percentage: %{customdata[1]:.2f}%<br>"  # Percentage value
        ),
        customdata=df_counts[['count', 'percentage']].values  # Pass count and percentage as custom data
    )

    st.plotly_chart(fig)
else:
    st.info("Please select at least one column for the hierarchy to generate the chart.")