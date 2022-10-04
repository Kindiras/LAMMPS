#This code generates the table potential for repulsive potential
import numpy as np
from datetime import date

def get_potential_Energy(x): #Becareful choosing the parameters here. This parameters are some examples, may not work for you
    return (0.105*(x-4.9)**2)
    
def get_force(x): #Negative the derivative of potential Energy
    return (-0.21*(x-4.9))

#It writes the table potential in Lammps requirement format
def write_potential_table(filename,N,R,v,f,today):
    with open(filename,'w') as ft:
        ft.write("# DATE: "+str(today)+ "  UNITS: metal")
        ft.write("\n")
        ft.write("# Repulsive Potential for Cd and Te: i,r,energy,force")
        ft.write("\n")
        ft.write("\n")
        ft.write("REPULSIVE")
        ft.write("\n")
        ft.write("N 90 R 2.2 4.9")
        ft.write("\n")
        ft.write("\n")
        for i in range(len(v)):
            ft.write(str(N[i]))
            ft.write(str(" "))
            ft.write(str(R[i]))
            ft.write(str(" "))
            ft.write(str(v[i]))
            ft.write(str(" "))
            ft.write(str(f[i]))
            ft.write("\n")


if __name__ == '__main__':
    today = date.today()
    N = []
    R = []
    V = []
    F = []
    n = 1
    for i in np.linspace(2.2,4.9,90): #linspace(start,rcut,total_points) do some research for start points, it should be smaller than nearest atoms distance when atoms oscillate 
        N.append(n)
        R.append(i)
        V.append(get_potential_Energy(i))
        F.append(get_force(i))
        n = n+1
    write_potential_table("CdTe_table",N,R,V,F,today)