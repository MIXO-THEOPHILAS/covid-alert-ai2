# main.py

import pandas as pd
import requests
from models.sird_model import run_simulation
import matplotlib.pyplot as plt

# 1. Fetch real COVID-19 data (South Africa as default)
def fetch_data(country="South Africa"):
    url = f"https://disease.sh/v3/covid-19/countries/{country}?strict=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "country": data["country"],
            "population": data["population"],
            "infected": data["active"],
            "recovered": data["recovered"],
            "deaths": data["deaths"]
        }
    else:
        raise Exception("Failed to fetch data")

# 2. Run the model
def simulate_covid(data):
    S0 = data["population"] - data["infected"] - data["recovered"] - data["deaths"]
    I0 = data["infected"]
    R0 = data["recovered"]
    D0 = data["deaths"]

    beta = 0.4
    gamma = 0.1
    mu = 0.01
    days = 60

    t, S, I, R, D = run_simulation(S0, I0, R0, D0, beta, gamma, mu, days)
    return t, S, I, R, D

# 3. Plot the results
def plot_results(t, S, I, R, D, country):
    plt.figure(figsize=(10,6))
    plt.plot(t, S, label='Susceptible')
    plt.plot(t, I, label='Infected')
    plt.plot(t, R, label='Recovered')
    plt.plot(t, D, label='Deaths')
    plt.xlabel('Days')
    plt.ylabel('Population')
    plt.title(f'SIRD Simulation for {country}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('covid_simulation.png')
    plt.show()

# 4. Alert if needed
def alert_check(I):
    peak_infected = max(I)
    threshold = 50000
    if peak_infected > threshold:
        print("⚠️ ALERT: Infection spike predicted!")
    else:
        print("✅ Infection under control.")

if __name__ == "__main__":
    covid_data = fetch_data("South Africa")
    t, S, I, R, D = simulate_covid(covid_data)
    plot_results(t, S, I, R, D, covid_data["country"])
    alert_check(I)
