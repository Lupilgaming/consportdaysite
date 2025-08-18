import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Load the CSV data
df = pd.read_csv("points.csv")

# Convert the 'datetime' column to datetime objects
df['datetime'] = pd.to_datetime(df['datetime'])

st.title("Athlete Performance Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")

# Date range filter
min_date = df['datetime'].min().date()
max_date = df['datetime'].max().date()

start_date = st.sidebar.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

# Ensure the end date is not before the start date
if start_date > end_date:
    st.sidebar.error("Error: End date must be after start date.")
    # Set end_date to start_date to prevent errors in the next step
    end_date = start_date

# Activity type filter
all_activity_types = df['activitytype'].unique().tolist()
selected_activity_types = st.sidebar.multiselect(
    "Select Activity Type(s)",
    options=all_activity_types,
    default=all_activity_types  # Default to all types selected
)

# Athlete name filter
all_athlete_names = df['athletename'].unique().tolist()
selected_athlete_names = st.sidebar.multiselect(
    "Select Athlete Name(s)",
    options=all_athlete_names,
    default=all_athlete_names  # Default to all athletes selected
)

# Apply all filters to the DataFrame
filtered_df = df[
    (df['datetime'].dt.date >= start_date) & 
    (df['datetime'].dt.date <= end_date) & 
    (df['activitytype'].isin(selected_activity_types)) &
    (df['athletename'].isin(selected_athlete_names))
]


# --- Dashboard Features (using filtered_df) ---

# 1. Leaderboard
st.header("Athlete Leaderboard")
leaderboard = filtered_df.groupby("athletename")["points"].sum().reset_index()
leaderboard = leaderboard.sort_values(by="points", ascending=False)
st.dataframe(leaderboard)

fig_leaderboard = px.bar(leaderboard, x="athletename", y="points", title="Leaderboard by Athlete")
st.plotly_chart(fig_leaderboard)

# 2. Main Activities by Points (for a selected athlete)
st.header("Main Activities by Points (per Athlete)")

# Ensure unique athlete names are available for the selectbox based on the filtered data
# If no athletes are selected in the multiselect, this will be empty, and the selectbox will be disabled.
if not filtered_df["athletename"].empty:
    selected_athlete_for_details = st.selectbox("Select Athlete for Activity Details", filtered_df["athletename"].unique())

    athlete_activities = filtered_df[filtered_df["athletename"] == selected_athlete_for_details].groupby("activitytype")["points"].sum().reset_index()
    athlete_activities = athlete_activities.sort_values(by="points", ascending=False)

    fig_activities = px.bar(athlete_activities, x="activitytype", y="points", title=f"Points by Activity Type for {selected_athlete_for_details}")
    st.plotly_chart(fig_activities)
else:
    st.write("No athlete data available for the selected filters.")


# 3. Activity Type Ranked by Average Points per Activity
st.header("Activity Type Ranking by Average Points")
avg_points_per_activity = filtered_df.groupby("activitytype")["points"].mean().reset_index()
avg_points_per_activity = avg_points_per_activity.sort_values(by="points", ascending=False)

fig_avg_points = px.bar(avg_points_per_activity, x="activitytype", y="points", title="Average Points per Activity Type")
st.plotly_chart(fig_avg_points)
