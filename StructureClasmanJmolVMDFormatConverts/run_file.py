"""Before using this program please check the following boundary conditions and the boxsize specially when \
 we convert xyz to clsman otherwise it may lead to wrong result"""

import os
def fileload(filename):
    with open(filename,"rt") as f:
      data = [[i for i in line.split()] for line in f.readlines()]
    return data


def filedumpj(filename,containts):
    with open(filename, "wt") as f:
       f.write(containts[0][0])
       f.write('\n')
       f.write('\n')
       for i in range(4,len(containts)):
            if(float(containts[i][2])<9.8):
                 f.write('Cu')
                 f.write('\t')
            else:
                 f.write('Zn')
                 f.write('\t')
            for j in range(3):
                f.write(str(containts[i][j]))
                f.write('\t')
            f.write('\n')
def chngdir(dirname):
    """Enter a path. If it does not exist, create one recursively and enter."""
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    os.chdir(dirname)            

def pbcxy(containts):
    dmin = 0.15
    dmaxx = float(containts[2][0]) -0.15
    dmaxy = float(containts[2][1]) -0.15
    for i in range(4,len(containts)):
        if (float(containts[i][0]) < - dmin):
             containts[i][0] = float(containts[i][0]) + float(containts[2][0])
        if (float(containts[i][0]) > dmaxx):
             containts[i][0] = float(containts[i][0]) - float(containts[2][0])
        if (float(containts[i][1]) < -dmin):
             (containts[i][1]) = float(containts[i][1]) + float(containts[2][1])
        if (float(containts[i][1]) > dmaxy):
            containts[i][1] = float(containts[i][1]) - float(containts[2][1])
    return containts  
def filedumpc(filename,containts,itype):
    with open(filename, "wt") as ft:
         m=0 
         ft.write("{0:5d}".format(int(containts[0][0])))
         ft.write ("{0:2d}".format(int(containts[0][1])))
         ft.write("{0:3d}".format(int(containts[0][1])))
         ft.write('\n')
         ft.write ('Fe/Cu(100) growth multiatom diffusion')
         ft.write('\n')
         ft.write("{0:20.8f}".format(float(containts[2][0])))           
         ft.write("{0:20.8f}".format(float(containts[2][1])))
         ft.write("{0:20.8f}".format(float(containts[2][2])))
         ft.write('\n')
         ft.write('(3f12.6,i2)')
         ft.write('\n')
         for i in range(4,len(containts)):
            for j in range (3):
                 ft.write("{0:12.6f}".format(float(containts[i][j])))
            ft.write(str("{0:2d}".format(int(itype[m]))))
            m=m+1 
            ft.write('\n')


"""To run from xyz to clsman first see the boxsize here and change to the appropriate boxsize"""
def filedumpxyz_clsman(filename,containts,itype):
     nn=1
     txaxis= 39.04200000 
     tyaxis= 39.04200000 
     tzaxis= 80.00000000
     with open(filename, "wt") as kt:
         m=0 
         kt.write("{0:5d}".format(int(containts[0][0])))
         kt.write ("{0:2d}".format(nn))
         kt.write("{0:3d}".format(nn))
         kt.write('\n')
         kt.write ('eminimizer')
         kt.write('\n')
         kt.write("{0:20.8f}".format(float(txaxis)))           
         kt.write("{0:20.8f}".format(float(tyaxis)))
         kt.write("{0:20.8f}".format(float(tzaxis)))
         kt.write('\n')
         kt.write('(3f12.6,i2)')
         kt.write('\n')
         for i in range(2,len(containts)):
            for j in range (1,4):
                 kt.write("{0:12.6f}".format(float(containts[i][j])))
            kt.write(str("{0:2d}".format(int(itype[m]))))
            m=m+1 
            kt.write('\n')

"""While marking the atoms see the z position and change it accordingly. Below is valid for one condition"""
def marking_atoms(data):
     itype = []
     for i in range (4, len(data)):
         z=float(data[i][2])
         if(z>11.6):
             if(z<12.8):
                itype.append(4)
         elif(z<11.6):
               if(z>10.2):
                 itype.append(2)
               else:
                   itype.append(data[i][3])        
         else:
              itype.append(data[i][3])  
     return itype  

"""This marking is to convert from xyz to clsman format, see the condition carefuly and \
 change the number below"""
def xyz_clsman_marking_atoms(data):
     itype = []
     for i in range (2, len(data)):
         z=float(data[i][3])
         if(z>10.1):
             itype.append(4)
         else:
             itype.append(1)         
     return itype  
      
  

            

