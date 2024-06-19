import pandas as pd
import numpy as np


def filter_team(df: pd.DataFrame, teams):
    """
    Filters the DataFrame for matches involving the specified teams.

    Parameters:
    df (pd.DataFrame):              The input DataFrame containing match data.
    teams (str or list of str):     The team(s) to filter by. Can be a single team as a string or multiple teams as a list of strings.

    Returns:
    pd.DataFrame: A DataFrame containing only the matches where the specified team(s) played as either the home or away team.

    Raises:
    ValueError: If the teams parameter is not a string or a list of strings, or if the teams are not present in the DataFrame.
    """
    if isinstance(teams, str):
        teams = [teams]
    if not isinstance(teams, list):
        raise ValueError("Teams should be a string or a list of strings")
    
    if any(team in df["home_team"].unique() or team in df["away_team"].unique() for team in teams):
        return df[(df["home_team"].isin(teams)) | (df['away_team'].isin(teams))]
    else:
        raise ValueError("One or more given teams are not available within the current set of filters")

def filter_tournament(df: pd.DataFrame, choices):    
    """
    Filters the DataFrame for matches from the specified tournaments.

    Parameters:
    df (pd.DataFrame):      The input DataFrame containing match data.
    choices (list of str):  The list of tournaments to filter by.

    Returns:
    pd.DataFrame: A DataFrame containing only the matches from the specified tournaments.
    """
    return df[df['tournament'].isin(choices)]

def filter_years(df: pd.DataFrame, year_range):
    """
    Filters the DataFrame for matches within the specified year range.

    Parameters:
    df (pd.DataFrame):      The input DataFrame containing match data.
    year_range (tuple):     A tuple specifying the start and end years (inclusive) to filter by.

    Returns:
    pd.DataFrame: A DataFrame containing only the matches within the specified year range.
    """
    start, end = year_range
    return df[(df["date"].dt.year >= start) & (df["date"].dt.year <= end)]

def filter_dataframe(df: pd.DataFrame, home_team=None, tournaments=None, opponents=None, year_range=None):
    """
    Filters the DataFrame based on multiple criteria including home team, tournaments, opponents, and year range.

    Parameters:
    df (pd.DataFrame):                          The input DataFrame containing match data.
    home_team (str or list of str, optional):   The team(s) to filter by for home matches.
    tournaments (list of str, optional):        The tournaments to filter by.
    opponents (str or list of str, optional):   The team(s) to filter by for opponent matches.
    year_range (tuple, optional):               A tuple specifying the start and end years (inclusive) to filter by.

    Returns:
    pd.DataFrame: A DataFrame filtered based on the specified criteria.
    """

    df = df.dropna()  # Drop missing values, e.g. games still to come
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
    """
    Calculates statistics for a specified team including wins, losses, draws, and total games played.

    Parameters:
    df (pd.DataFrame):  The input DataFrame containing match data.
    team (str):         The team to calculate statistics for.

    Returns:
    dict: A dictionary containing the number of wins, losses, draws, and total games played by the specified team.
    """
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
    
def team_won(df, team):
    """
    Identifies the indices of matches where the specified team won.

    Parameters:
    df (pd.DataFrame):  The input DataFrame containing match data.
    team (str):         The team to identify wins for.

    Returns:
    pd.Index:           An index object containing the indices of the matches where the specified team won.
    """

    # Find indices where the team won as home team
    home_wins = df[(df['home_team'] == team) & (df['home_score'] > df['away_score'])].index
    
    # Find indices where the team won as away team
    away_wins = df[(df['away_team'] == team) & (df['away_score'] > df['home_score'])].index
    
    # Combine the indices
    won_indices = home_wins.union(away_wins)
    
    return won_indices

def highlight_wins(s, won_indices):
    """
    Highlights the rows in a DataFrame where the specified team won.

    Parameters:
    s (pd.Series):          A series object representing a row in the DataFrame.
    won_indices (pd.Index): An index object containing the indices of the matches where the specified team won.

    Returns:
    list: A list of strings representing the CSS styles to apply to the row. Rows where the team won are highlighted.
    """

    if s.name in won_indices:
        return ['background-color: rgba(0, 255, 0, 0.1)'] * len(s)
    else:
        return [''] * len(s)