import streamlit
import pandas as pd
import numpy as np


def filter_team(df: pd.DataFrame, teams):
    if isinstance(teams, str):
        teams = [teams]
    if not isinstance(teams, list):
        raise ValueError("Teams should be a string or a list of strings")
    
    if any(team in df["home_team"].unique() or team in df["away_team"].unique() for team in teams):
        return df[(df["home_team"].isin(teams)) | (df['away_team'].isin(teams))]
    else:
        raise ValueError("One or more given teams are not available within the current set of filters")

def filter_tournament(df: pd.DataFrame, choices):    
    return df[df['tournament'].isin(choices)]

def filter_years(df: pd.DataFrame, year_range):
    start, end = year_range
    return df[(df["date"].dt.year >= start) & (df["date"].dt.year <= end)]

def filter_dataframe(df: pd.DataFrame, home_team=None, tournaments=None, opponents=None, year_range=None):
    if home_team:
        df = filter_team(df, home_team)
    if tournaments:
        df = filter_tournament(df, tournaments)
    if opponents:
        df = filter_team(df, opponents)
    if year_range:
        df = filter_years(df, year_range)
    
    return df


def calculate_team_stats(df, team):
    if team:
        # Convert relevant columns to NumPy arrays
        home_teams = df['home_team'].values
        away_teams = df['away_team'].values
        home_scores = df['home_score'].values
        away_scores = df['away_score'].values
        
        # Determine the matches involving the specified team
        is_home_team = home_teams == team
        is_away_team = away_teams == team
        
        # Calculate wins, losses, and draws
        wins = np.sum((is_home_team & (home_scores > away_scores)) | (is_away_team & (away_scores > home_scores)))
        losses = np.sum((is_home_team & (home_scores < away_scores)) | (is_away_team & (away_scores < home_scores)))
        draws = np.sum((is_home_team & (home_scores == away_scores)) | (is_away_team & (away_scores == home_scores)))
        total_games = np.sum([wins, losses, draws])
        return {'wins': wins, 'losses': losses, 'draws': draws, 'total_games': total_games}
    
    else:
        return None

