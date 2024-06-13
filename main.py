import streamlit as st
import pandas as pd

st.title('EURO 2024 :soccer:')

@st.cache_data
def load_data():
    df_goals = pd.read_csv('data/goalscorers.csv')
    df_results = pd.read_csv('data/results.csv')
    df_shootouts = pd.read_csv('data/shootouts.csv')
    return df_goals, df_results, df_shootouts

add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

df_goals, df_results, df_shootouts = load_data()

left, right = st.columns(2)

with left:
    st.text_input("What is your name?: ", key="name")
    st.write(f'HA, you said {st.session_state.name}')

with right:
    checkbox = st.checkbox('Show table: ')
    if checkbox:
        country = st.selectbox('country', options=df_results['home_team'].unique())
        df_nl = df_results[(df_results['home_team'] == country) | (df_results['away_team'] == country)]
        df_nl

st.subheader('Best scorers internationals')
top_scorers = df_goals.groupby(by='scorer').size().reset_index(name='counts').sort_values('counts', ascending=False)
top_scorers = top_scorers.set_index('scorer')
st.bar_chart(top_scorers['counts'][:10])