import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
# import matplotlib.pyplot as plt

from funcs import filter_dataframe, calculate_team_stats

st.title('EURO 2024 :soccer:')

@st.cache_data
def load_data():
    """
    A function that loads the data from csv and caches it so it can be shared accross sessions
    """
    df_goals = pd.read_csv('data/goalscorers.csv')
    df_results = pd.read_csv('data/results.csv')
    df_shootouts = pd.read_csv('data/shootouts.csv')

    df_goals['date'] = pd.to_datetime(df_goals['date'], format='%Y-%m-%d')
    df_results['date'] = pd.to_datetime(df_results['date'], format='%Y-%m-%d')
    df_shootouts['date'] = pd.to_datetime(df_shootouts['date'], format='%Y-%m-%d')

    return df_goals, df_results, df_shootouts

df_goals, df_results, df_shootouts = load_data()


# Sidebar area
# ------------------------------

teams = df_results["home_team"].sort_values().unique().tolist()
idx_nl = teams.index('Netherlands') if 'Netherlands' in teams else 0
team = st.sidebar.selectbox(
    'What team would you like to see the stats from?',
    teams,
    index=idx_nl,
)

tournaments = st.sidebar.multiselect(
    "Filter tournament?", 
    list(df_results[(df_results['home_team'] == team) | (df_results['away_team'] == team)].tournament.unique())
    )

opponents = st.sidebar.multiselect(
    'Against a specific team or teams?',
    df_results["home_team"].unique()
)

min_value = df_results[(df_results['home_team'] == team) | (df_results['away_team'] == team)]['date'].dt.year.min()
max_value = df_results['date'].dt.year.max()

years = st.sidebar.slider(
    "During which years?", 
    min_value=min_value,
    max_value=max_value,
    value=(min_value, max_value)
)
# ------------------------------

# filter the results
df_results = filter_dataframe(df_results, home_team=team, tournaments=tournaments, opponents=opponents, year_range=years)

# ------------------------------
st.subheader('Top 10 scorers!')
top_scorers = df_goals[df_goals['team'] == team].merge(
    df_results[['date', 'home_team', 'away_team']],
    on=['date', 'home_team', 'away_team'],
    how='inner'
)
top_scorers = top_scorers.groupby(by='scorer').size().reset_index(name='counts')
top_scorers = top_scorers.sort_values('counts', ascending=False)[:10]
# top_scorers = top_scorers.set_index('scorer')

bar_chart = alt.Chart(top_scorers[:10]).mark_bar().encode(
    x=alt.X('counts:Q', title='Count of Goals'),
    y=alt.Y('scorer:N', sort='-x', title='Name of the Player')
)

# Display the bar chart in Streamlit
st.altair_chart(bar_chart, use_container_width=True)
# ------------------------------

# ------------------------------
st.subheader('Historical Statistics')
outcome = calculate_team_stats(df=df_results, team=team)
if outcome:
    col1, col2, col3 = st.columns(3)    
    win_ratio = round(outcome['wins'] / outcome['total_games'] * 100, 1)
    lose_ratio = round(outcome['losses'] / outcome['total_games'] * 100, 1)
    draw_ratio = round(outcome['draws'] / outcome['total_games'] * 100, 1)
    win_label = ':green-background[Win Percentage]' if win_ratio > 50 else ':red-background[Win Percentage]'
    
    col1.metric(win_label, f'{win_ratio}%')
    col2.metric("Losing Percentage", f'{lose_ratio}%')
    col3.metric("Draw Percentage", f'{draw_ratio}%')

# ------------------------------
