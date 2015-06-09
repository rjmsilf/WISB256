import numpy as np
import scipy as sp
from scipy.linalg import eigvals
from scipy.integrate import odeint

class Lorenz:

    def __init__(self,lijst, sigma=10, rho=28, beta=(8/3)):
        self.x_0=lijst[0]
        self.y_0=lijst[1]
        self.z_0=lijst[2]
        self.sigma=sigma
        self.rho=rho
        self.beta=beta


    def functies(self,ODE,t):
        x_dot=self.sigma*(ODE[1]-ODE[0])
        y_dot=ODE[0]*(self.rho-ODE[2])-ODE[1]
        z_dot=ODE[0]*ODE[1]-self.beta*ODE[2]
        return np.array([x_dot,y_dot,z_dot])

    def solve(self,T,dt):
        self.times=np.arange(0,T,dt)
        self.initialisatie=[self.x_0,self.y_0,self.z_0]
        self.antwoord = odeint(self.functies,self.initialisatie,self.times)
        return self.antwoord