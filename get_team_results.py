import json
import os
import matplotlib.pyplot as plt
import streamlit as st

# Função para carregar os dados das partidas
def load_matches(competition_id, season_id):
    """
    Carrega os dados das partidas para uma competição e temporada específicas.
    """
    file_path = os.path.join("open-data-master", "data", "matches", str(competition_id), str(season_id))
    try:
        with open(f"{file_path}.json", "r", encoding="utf-8") as f:
            matches = json.load(f)
        return matches
    except FileNotFoundError:
        st.error(f"Arquivo não encontrado: {file_path}.json")
        return []

# Função para filtrar partidas de um time específico
def filter_team_matches(matches, team_name):
    """
    Filtra as partidas de um time específico (mandante ou visitante).
    Separa os resultados em casa e fora.
    """
    home_results = {"win": 0, "draw": 0, "loss": 0, "goals_for": 0, "goals_against": 0}
    away_results = {"win": 0, "draw": 0, "loss": 0, "goals_for": 0, "goals_against": 0}

    for match in matches:
        home_team = match["home_team"]["home_team_name"]
        away_team = match["away_team"]["away_team_name"]
        home_score = match["home_score"]
        away_score = match["away_score"]

        if home_team == team_name:  # Partida em casa
            home_results["goals_for"] += home_score
            home_results["goals_against"] += away_score
            if home_score > away_score:
                home_results["win"] += 1
            elif home_score < away_score:
                home_results["loss"] += 1
            else:
                home_results["draw"] += 1

        elif away_team == team_name:  # Partida fora
            away_results["goals_for"] += away_score
            away_results["goals_against"] += home_score
            if away_score > home_score:
                away_results["win"] += 1
            elif away_score < home_score:
                away_results["loss"] += 1
            else:
                away_results["draw"] += 1

    return home_results, away_results

# Função para calcular métricas de desempenho
def calculate_metrics(home_results, away_results):
    """
    Calcula métricas de desempenho para um time.
    """
    total_home_matches = sum([home_results[key] for key in ["win", "draw", "loss"]])
    total_away_matches = sum([away_results[key] for key in ["win", "draw", "loss"]])
    total_matches = total_home_matches + total_away_matches

    win_rate = ((home_results["win"] + away_results["win"]) / total_matches) * 100 if total_matches > 0 else 0
    draw_rate = ((home_results["draw"] + away_results["draw"]) / total_matches) * 100 if total_matches > 0 else 0
    loss_rate = ((home_results["loss"] + away_results["loss"]) / total_matches) * 100 if total_matches > 0 else 0

    goals_for = (home_results["goals_for"] + away_results["goals_for"]) / total_matches if total_matches > 0 else 0
    goals_against = (home_results["goals_against"] + away_results["goals_against"]) / total_matches if total_matches > 0 else 0

    return win_rate, draw_rate, loss_rate, goals_for, goals_against

# Função para prever resultados de uma partida hipotética
def predict_match_outcome(team1_metrics, team2_metrics):
    """
    Prevê as probabilidades de vitória, empate e derrota em uma partida hipotética.
    """
    team1_win_prob = (
        (team1_metrics[0] + team2_metrics[2]) / 2 +  # Vitórias do time 1 + Derrotas do time 2
        (team1_metrics[3] - team2_metrics[4]) / 2    # Gols marcados pelo time 1 - Gols sofridos pelo time 2
    )
    team2_win_prob = (
        (team2_metrics[0] + team1_metrics[2]) / 2 +  # Vitórias do time 2 + Derrotas do time 1
        (team2_metrics[3] - team1_metrics[4]) / 2    # Gols marcados pelo time 2 - Gols sofridos pelo time 1
    )
    draw_prob = (team1_metrics[1] + team2_metrics[1]) / 2  # Média de empates

    # Normalizar as probabilidades para somar 100%
    total_prob = team1_win_prob + team2_win_prob + draw_prob
    team1_win_prob = (team1_win_prob / total_prob) * 100
    team2_win_prob = (team2_win_prob / total_prob) * 100
    draw_prob = (draw_prob / total_prob) * 100

    return team1_win_prob, draw_prob, team2_win_prob

# Configurações iniciais do Streamlit
st.title("Dashboard Interativo de Previsão de Partidas")

# Entrada de dados do usuário
competition_id = st.number_input("ID da Competição:", value=9)
season_id = st.number_input("ID da Temporada:", value=27)

# Carregar os dados das partidas
matches = load_matches(competition_id, season_id)

# Extrair todos os times únicos da competição
if matches:
    all_teams = set()
    for match in matches:
        all_teams.add(match["home_team"]["home_team_name"])
        all_teams.add(match["away_team"]["away_team_name"])
    all_teams = sorted(all_teams)

    # Selecionar times usando selectbox
    team_name_1 = st.selectbox("Selecione o Primeiro Time:", options=all_teams)
    team_name_2 = st.selectbox("Selecione o Segundo Time:", options=all_teams)

    if st.button("Gerar Dashboard"):
        # Filtrar partidas dos times
        home_results_1, away_results_1 = filter_team_matches(matches, team_name_1)
        home_results_2, away_results_2 = filter_team_matches(matches, team_name_2)

        # Calcular métricas de desempenho
        metrics_1 = calculate_metrics(home_results_1, away_results_1)
        metrics_2 = calculate_metrics(home_results_2, away_results_2)

        # Prever o resultado da partida
        team1_win_prob, draw_prob, team2_win_prob = predict_match_outcome(metrics_1, metrics_2)

        # Exibir os nomes dos times lado a lado
        col1, col2 = st.columns(2)
        with col1:
            st.header(team_name_1)
            st.write(f"Taxa de Vitórias: {metrics_1[0]:.2f}%")
            st.write(f"Taxa de Empates: {metrics_1[1]:.2f}%")
            st.write(f"Taxa de Derrotas: {metrics_1[2]:.2f}%")
            st.write(f"Média de Gols Marcados: {metrics_1[3]:.2f}")
            st.write(f"Média de Gols Sofridos: {metrics_1[4]:.2f}")

        with col2:
            st.header(team_name_2)
            st.write(f"Taxa de Vitórias: {metrics_2[0]:.2f}%")
            st.write(f"Taxa de Empates: {metrics_2[1]:.2f}%")
            st.write(f"Taxa de Derrotas: {metrics_2[2]:.2f}%")
            st.write(f"Média de Gols Marcados: {metrics_2[3]:.2f}")
            st.write(f"Média de Gols Sofridos: {metrics_2[4]:.2f}")

        # Criar gráficos comparativos
        labels = ["Vitórias", "Empates", "Derrotas"]
        team1_values = [metrics_1[0], metrics_1[1], metrics_1[2]]
        team2_values = [metrics_2[0], metrics_2[1], metrics_2[2]]

        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(labels))
        ax.bar(x, team1_values, width=0.4, label=team_name_1, align="center")
        ax.bar([p + 0.4 for p in x], team2_values, width=0.4, label=team_name_2, align="center")
        ax.set_xlabel("Métricas")
        ax.set_ylabel("Valores (%)")
        ax.set_title("Comparação de Desempenho")
        ax.set_xticks([p + 0.2 for p in x])
        ax.set_xticklabels(labels)
        ax.legend()
        st.pyplot(fig)

        # Exibir a previsão final
        st.subheader("Previsão de Resultado")
        st.write(f"Probabilidade de Vitória ({team_name_1}): {team1_win_prob:.2f}%")
        st.write(f"Probabilidade de Empate: {draw_prob:.2f}%")
        st.write(f"Probabilidade de Vitória ({team_name_2}): {team2_win_prob:.2f}%")