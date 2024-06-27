# Importing the required packages
# ------------------------------
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import folium
from streamlit_folium import st_folium
from country_coords import country_coords

from funcs import load_data, get_win_ratio, filter_dataframe, calculate_team_stats, team_won, highlight_wins

#Page configurations including favicon and title
st.set_page_config(
    page_title='International Football Statistics',
    page_icon="./assets/icons8-football-ball-pastel-96.png"
)

# Loading the data
# ------------------------------
df_goals, df_results, df_shootouts, df_locations = load_data()
df_temp = pd.DataFrame(pd.concat([df_results['home_team'], df_results['away_team']]).unique())
df_temp.to_csv('./temp.csv')

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
    df_results[(df_results['home_team'] == team) | (df_results['away_team'] == team)]["home_team"].unique()
)

min_value = df_results[(df_results['home_team'] == team) | (df_results['away_team'] == team)]['date'].dt.year.min()
max_value = df_results['date'].dt.year.max()

years = st.sidebar.slider(
    "During which years?", 
    min_value=min_value,
    max_value=max_value,
    value=(1980 if 1980 > min_value else min_value, max_value)
)

# Filter the results based on sidebar
# ------------------------------

df_res_filtered = filter_dataframe(df_results, home_team=team, tournaments=tournaments, opponents=opponents, year_range=years)

# Graph showing the top 10 scorers for the country
# ------------------------------

st.title(f'Football stats of {team} :soccer:')

st.subheader('Top 10 scorers!')
top_scorers = df_goals[df_goals['team'] == team].merge(
    df_res_filtered[['date', 'home_team', 'away_team']],
    on=['date', 'home_team', 'away_team'],
    how='inner'
)
top_scorers = top_scorers.groupby(by='scorer').size().reset_index(name='counts')
top_scorers = top_scorers.sort_values('counts', ascending=False)[:10]

bar_chart = alt.Chart(top_scorers[:10]).mark_bar().encode(
    x=alt.X('counts:Q', title='Count of Goals'),
    y=alt.Y('scorer:N', sort='-x', title='Name of the Player'),
    color=alt.Color('counts:Q', scale=alt.Scale(scheme='oranges'), legend=None)
)

st.altair_chart(bar_chart, use_container_width=True)

# KPI from game statistics
# ------------------------------
st.subheader('Game Statistics')
outcome = calculate_team_stats(df=df_res_filtered, team=team)
if outcome:
    col1, col2, col3 = st.columns(3)    
    win_ratio = round(outcome['wins'] / outcome['total_games'] * 100, 1)
    lose_ratio = round(outcome['losses'] / outcome['total_games'] * 100, 1)
    draw_ratio = round(outcome['draws'] / outcome['total_games'] * 100, 1)
    win_label = ':green-background[Win Percentage]' if win_ratio > 50 else ':red-background[Win Percentage]'
    
    col1.metric(win_label, f'{win_ratio}%')
    col2.metric("Losing Percentage", f'{lose_ratio}%')
    col3.metric("Draw Percentage", f'{draw_ratio}%')

# Total win percentage per year versus win percentage of filters
# ------------------------------
st.subheader('Win Percentage Per Year')
df_results_year = df_res_filtered.groupby(df_res_filtered['date'].dt.year)
df_results_total = filter_dataframe(df_results, home_team=team, year_range=years)
df_results_total = df_results_total.groupby(df_results_total['date'].dt.year)
years_filtered = []
win_pct_filtered = []
years_total = []
win_pct_total = []

for year, df in df_results_year:
    won_indices = team_won(df, team=team)
    total_games = df[~df['home_score'].isna()].shape[0]
    if total_games:
        win_pct = round(len(won_indices) / df[~df['home_score'].isna()].shape[0] * 100, 1)
    else:
        win_pct = 0.0
    win_pct_filtered.append(win_pct)
    years_filtered.append(year)

for year, df in df_results_total:
    won_indices = team_won(df, team=team)
    total_games = df[~df['home_score'].isna()].shape[0]
    if total_games:
        win_pct = round(len(won_indices) / df[~df['home_score'].isna()].shape[0] * 100, 1)
    else:
        win_pct = 0.0
    win_pct_total.append(win_pct)
    years_total.append(year)


# Create DataFrames for plotting
df_plot_filter = pd.DataFrame({"Year": years_filtered, "Win Percentage": win_pct_filtered, "Type": "Filtered"})
df_plot = pd.DataFrame({"Year": years_total, "Win Percentage": win_pct_total, "Type": "Total"})

# Combine DataFrames
df_combined = pd.concat([df_plot_filter, df_plot])

# Create the Altair line chart with both lines and a legend
line_chart = alt.Chart(df_combined).mark_line().encode(
    x=alt.X('Year:O', title='Year'),
    y=alt.Y('Win Percentage:Q', title='Win Percentage', scale=alt.Scale(domain=[0, 100])),
    color=alt.Color('Type:N', title='Type', scale=alt.Scale(domain=['Filtered', 'Total'], range=['#FFA07A', '#FF4500'])),  # Lighter and darker shades of orange
    tooltip=['Year', 'Win Percentage', 'Type']
)

# Create points for filtered data with the same lighter orange color
points_filtered = alt.Chart(df_plot_filter).mark_point(size=100, filled=True).encode(
    x=alt.X('Year:O'),
    y=alt.Y('Win Percentage:Q'),
    color=alt.value('#FFA07A')  # Lighter orange color for the points
)

# Combine the line chart with the points
combined_chart = alt.layer(line_chart, points_filtered).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=16
).configure_legend(
    titleFontSize=14,
    labelFontSize=12
)

st.altair_chart(combined_chart, use_container_width=True)

# Games played over the time range per tournament
# ------------------------------
st.subheader(f'Games per Tournament from {years[0]} to {years[1]}')
games_tournament = df_res_filtered.groupby('tournament').size().reset_index(name='count').sort_values(by='count', ascending=False)

bar_chart = alt.Chart(games_tournament).mark_bar().encode(
    x=alt.X('count:Q', title='Count of Games'),
    y=alt.Y('tournament:N', sort='-x', title='Tournament'),
    color=alt.Color('count:Q', scale=alt.Scale(scheme='oranges'), legend=None)
)

# Display the bar chart in Streamlit
st.altair_chart(bar_chart, use_container_width=True)

# Last ten matches displayed in a table
# ------------------------------
st.subheader('Last Ten Matches')
df_10 = df_res_filtered.drop(['city', 'country', 'neutral'], axis=1)
df_10 = df_10.sort_values(by='date', ascending=False)
df_10 = df_10[df_10['date'] <= datetime.now()].head(10)
df_10['date'] = df_10['date'].dt.date
df_10[['home_score', 'away_score']] = df_10[['home_score', 'away_score']].astype(int)
df_10 = df_10.style.apply(highlight_wins, won_indices=team_won(df_10, team=team), axis=1)
st.dataframe(df_10, hide_index=True, use_container_width=True)

# World map
# ---------

df_locations = get_win_ratio(df_res_filtered, df_locations, team)
st.dataframe(df_locations)

# Function to map win ratio to color
def win_ratio_to_color(win_ratio):
    if win_ratio > 0.75:
        return 'darkgreen'
    elif win_ratio > 0.5:
        return 'lightgreen'
    elif win_ratio > 0.25:
        return 'orange'
    else:
        return 'red'

# Create a base map
m = folium.Map(location=[20, 0], zoom_start=2)

# Add countries to the map
for idx, row in df_locations.iterrows():
    if row['win_ratio']:
        folium.CircleMarker(
            location=(row['lat'], row['lon']),
            radius=10,
            color=win_ratio_to_color(row['win_ratio']),
            fill=True,
            fill_color=win_ratio_to_color(row['win_ratio']),
            fill_opacity=0.6,
            popup=f"{row['country']}: {row['win_ratio'] * 100:.2f}%"
        ).add_to(m)

# Display the map in Streamlit
st.title('Win Ratios by Country')
st_folium(m, width=800, height=500)
