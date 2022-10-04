import os
import argparse
from runnew_conf import atoms_position, filedumpc,filedumpj
parser=argparse.ArgumentParser()
parser.add_argument('-t','--ftype',help='format for clsman or zyz',choices = ['clsman','xyz'])
args = parser.parse_args()
if __name__ == '__main__':
    strainx=float(input("what is x-strain? could be 1.04 for tensile 4 per or 0.96 for compressive 4 per or 1 for no strain "))
    strainy=float(input("what is y-strrain?"))
    lattice=float(input("what is the lattice constant?"))
    lsize=int(input("what is configuration size like 20 for 10xa where a is lattice constant?"))
    layers=int(input("how many layers you want like 5 for 5 layers?"))
    filename=input("what is the file name lke data.dat for clsman or data.xyz for xyz format?")
    position, itype, ia = atoms_position (strainx,strainy,lsize,lattice,layers)
    if args.ftype == "clsman":
     	filedumpc(filename,ia,position, itype,lsize,strainx,strainy,lattice)
    else:
        filedumpj(filename,position,ia)
     
