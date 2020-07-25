import numpy as np
from numpy import zeros,cos,tan,log,exp,sqrt,pi,clip,real,argwhere,append,linspace,squeeze,isscalar,save
from scipy.integrate import quad
import numba
from numba import jit,njit
from numba import cfunc,carray
from numba.types import intc, CPointer, float64

import matplotlib.pyplot as plt


@njit
def clip(x,low=-1e80,up=1e80):
    return max(min(up,x),low)
@njit
def sec(x):
    return 1.0/cos(x)

@njit
def xi(eta,u):
    q =(1+eta)/(1-eta)
    q =clip(q)
    f = (log(q)+1j*u)/(eta+1j*tan(u/2))#
    return f

@njit
def phi_pt1(r,t):
    eta=r/t
    q =(1+eta)/(1-eta)
    q =clip(q)
    y = exp(-t)/(4*pi*r*t**2)*t*log(q)
    return y


@njit
def integrand_pt(u,eta,t):
            return sec(u/2)**2*real(
           (eta+1j*tan(u/2))*xi(eta,u)**3
           *exp(t/2*(1-eta**2)*xi(eta,u)))

def phi_pt(r,t):
    r = clip(r,1e-10,1e80)
    eta = r/t
    g = 0.0
    if eta<1.0:
        g,_ = quad(integrand_pt,0,pi,args=(eta,t,),epsabs=1e-2)
    f = 1/(2*pi)*exp(-t) /(4*pi*r*t**2)*(t/2)**2*(1-eta**2)*g
    f = f + phi_pt1(r,t)
    return f

def phi_l_single(eta,t):
    integrand = lambda w: phi_pt(t*sqrt(eta**2+w**2),t)
    f,_ =quad(integrand,0,sqrt(1-eta**2),epsabs=1e-5)
    phi_l0 = exp(-t)/(2*pi*t**2) / sqrt(1-eta**2)
    f = phi_l0 + (2*t)*f
    return f

def phi_l(t,rho):
    
    # Make sure this works with almost any dimensions
    if isscalar(t):
        t = t*np.ones(rho.shape)
    if isscalar(rho):
        rho = rho*np.ones(t.shape)
            
    eta = rho/t
    ind = squeeze(argwhere(eta<1))
    f = zeros(eta.shape)
    
    for k in ind:
        f[k] = phi_l_single(eta[k],t[k])

    return f
def phi_lv2(t,rho):    
    # Make sure this works with almost any dimensions
    eta = rho/t
    if eta<1:
        return phi_l_single(eta,t)
    else:
        return 0.0

def pathintegral(x,y,omegax,omegay,t,sigmaa,sigmas):
    
    def integrand(tau):
        return (
                sigmas*exp(-(sigmaa+sigmas)*tau)
                    *phi_lv2(tau,sqrt((x-tau*omegax)**2+(y-tau*omegay)**2))
               )

    result = quad(integrand,0,t,epsabs=1e-5)
    return result



def getls(n):
    r = np.linspace(0,1.6,n)
    phi = phi_l(1.0,r)
    r = np.append(-r[::-1][:-1],r)
    phi = np.append(phi[::-1][:-1],phi)
    ls = np.zeros((len(r),2))
    return np.vstack((r,phi)).T
