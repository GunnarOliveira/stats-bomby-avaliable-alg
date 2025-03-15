# StatsBomb Match Prediction Dashboard 📊⚽

This project is a solution to visualize and analyze football data using **StatsBomb's open datasets**.  
The goal is to create an interactive dashboard that predicts the outcome of hypothetical matches based on historical data.

## Project Structure 📂

- **`open-data-master/`**: Contains the raw JSON files from StatsBomb.
  - **`data/events/`**: Includes detailed event data for matches (e.g., passes, shots, tackles).
  - **`data/lineups/`**: Includes lineup information for each match (e.g., starting XI, substitutions).
  - **`data/matches/`**: Includes match metadata for different competitions and seasons.
  - **`data/three-sixty/`**: Includes advanced tracking data for matches (if available).
  - **`data/competitions.json`**: Metadata about competitions and seasons.
- **`get_team_results.py`**: Houses the main processing script to calculate team performance metrics.
- **`requirements.txt`**
- **`README.md`**: Documentation of the project.

## 📌 Features

- **Interactive Dashboard**: Built using Streamlit for user-friendly interaction.
- **Historical Data Analysis**: Analyze team performance metrics like win rate, goals scored, and goals conceded.
- **Match Prediction**: Predict the outcome of hypothetical matches between two teams.
- **Visual Comparisons**: Compare team performance metrics using bar charts and tables.

## 🛠️ Technologies Used

- **Python**: For data parsing, analysis, and visualization.
  - Libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `streamlit`
- **Streamlit**: For creating the interactive dashboard.
- **JSON**: To handle StatsBomb's raw data files.
- **Matplotlib**: For generating bar charts and other visualizations.


## Installation & Usage 📥

1. Clone this repository:

```bash
git clone https://github.com/GunnarOliveira/statsbomb-prediction-dashboard.git
```

2. Navigate to the project directory:
   
```bash
cd statsbomb-prediction-dashboard
```

3. Install the required dependencies:
   
```bash
pip install -r requirements.txt
```

4. Run the Streamlit app locally:
   
```bash
streamlit run get_team_results.py
```
