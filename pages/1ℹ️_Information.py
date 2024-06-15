import streamlit as st

# Function to read the content of the README.md file
def read_markdown_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()

# Path to the README.md file
readme_file = './README.md'

# Read the content of the README.md file
readme_content = read_markdown_file(readme_file)

# Display the content of the README.md file in Streamlit
st.markdown(readme_content)
