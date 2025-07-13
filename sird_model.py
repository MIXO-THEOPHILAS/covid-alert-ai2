# models/sird_model.py

import numpy as np
from scipy.integrate import odeint

def sird_model(y, t, beta, gamma, mu):
    S, I, R, D = y
    N = S + I + R + D
    dS_dt = -beta * S * I / N
    dI_dt = beta * S * I / N - gamma * I - mu * I
    dR_dt = gamma * I
    dD_dt = mu * I
    return [dS_dt, dI_dt, dR_dt, dD_dt]

def run_simulation(S0, I0, R0, D0, beta, gamma, mu, days):
    y0 = [S0, I0, R0, D0]
    t = np.linspace(0, days, days)
    ret = odeint(sird_model, y0, t, args=(beta, gamma, mu))
    S, I, R, D = ret.T
    return t, S, I, R, D
