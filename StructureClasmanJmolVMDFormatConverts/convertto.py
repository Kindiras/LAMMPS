import os
import argparse
from glob import glob
from run_file import fileload, filedumpj, chngdir, pbcxy, \
     filedumpc, marking_atoms, filedumpxyz_clsman, xyz_clsman_marking_atoms
parser = argparse.ArgumentParser()
parser.add_argument('-t','--ftype', help='format for clsman and jmol or vmd', choices = ['clsman','jmol','xyztoclsman'])
args = parser.parse_args()
"""This program helps to convert the files into xyz or clsman or xyz to clsman \
format using boundary condition"""
if __name__ == '__main__':
     if args.ftype == "xyztoclsman":
         dir_list = glob("*.xyz")
         for i in dir_list:
             kk=fileload(i)
             chngdir("convertedfiles")
             atom =  xyz_clsman_marking_atoms(kk)
             filedumpxyz_clsman(str(i)+".dat",kk, atom) 
             os.chdir('../')
     else:   
         dir_list=glob("*.dat") 
         for i in dir_list:
             kk=fileload(i)
             chngdir("convertedfiles")
             pb=pbcxy(kk)
             if args.ftype == "jmol":
                 filedumpj(str(i)+".xyz",pb)
             elif args.ftype == "clsman":
                 atom = marking_atoms(pb)
                 filedumpc(str(i)+".dat",kk, atom)
             os.chdir('../') 
            
