# ⚽ Football Statistics Dashboard

Welcome to the Football Statistics Dashboard project! This project provides an interactive web application to explore and analyze football statistics using Streamlit. The app includes various features such as top scorers, historical statistics, win percentages, and recent match results. The data originates from the [International football results from 1872 to 2024](https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017) dataset on Kaggle. Thanks to Mart Jürisoo for making this dataset available.

The goal of the project is to deploy my first application in the cloud via Azure to apply my knowledge gathered from the [AZ-900: Azure fundamentals](https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/?practice-assessment-type=certification) certificate.

The project is a work-in-progress and will change during the course of the UEFA EURO's 2024. I would like to invite others to join this project, please see the [Contributing](#contributing) section for more details. 

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Usage](#usage)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview

The Football Statistics Dashboard is an interactive web application designed to provide insights into football match data per country. Users can filter data by team, tournament, opponents, and year range to view specific statistics. The app includes visualizations to help users understand the data better.

## Features

- **Top Scorers**: View the top 10 scorers for a selected team per league and/or opponent.
- **Historical Statistics**: Analyze win, loss, and draw percentages for a selected team per league and/or opponent.
- **Win Percentage Per Year**: Visualize the win percentage of a team over different years per league and/or opponent.
- **Recent Matches**: Display the last ten matches of the selected team with results highlighted per league and/or opponent.

## Usage

### Website

To use the website:
1. Select a team from the sidebar to view its statistics.
2. Use the filters to narrow down the data by tournament, opponents, and year range.
3. Explore the different sections for top scorers, historical statistics, win percentages, and recent matches.

### Local Installation

If you want to run the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/football-stats-dashboard.git
   cd football-stats-dashboard

2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the dependencies**
    ```bash
    pip install -r requirements.txt

4. **Run the Streamlit app**
    ```bash
    streamlit run ⚽_Football_Statistics.py

5. **Access the app**
    Open your browser and go to: `http://localhost:8501`.

## Contributing

I want to welcome contributions (especially first timers)! It can be hard to find first projects to work on. If you only want to change some text or go all-out, I'm open for it :happy:. Once I accept your pull-request you can immediately see the results on the webpage!

To contribute please follow the following steps:

1. **Fork the repository on [GitHub](https://github.com/SammieKn/EKStatistics)**

2. **Clone your forked repository** to your local machine.

3. **Create a new branch for your changes**
    ```bash
    git checkout -b feature-branch

4. **Make your changes** and commit them.
    ```bash
    git add .
    git commit -m "Describe your changes"

5. **Push your changes** to your forked repository.
    ```bash
    git push origin feature-branch

6. **Create a pull request** to the main repository.

## License

This project is licensed under the MIT License. See the [License](https://github.com/SammieKn/EKStatistics/blob/master/LICENSE) file for more details.





