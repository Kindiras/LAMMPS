import os
def atoms_position(strainx,strainy,lsize,lattice,layers):
     Lsize = lsize
     strainx = strainx
     strainy=strainy
     bag = lattice/2
     xlat = bag*strainx
     ylat = bag*strainy
     txaxes = Lsize*bag*strainx
     tyaxes = Lsize*bag*strainy
     tzaxes = 80
     layeradd = layers
     tot=int(Lsize*Lsize/2)*layeradd
     ia=0
     itype=[]
     containts = [[0 for i in range(0,tot+1)] for j in range(0,tot+1)]
     for k in range(layeradd, 0, -1):
	     for i in range(0,Lsize):
	       	for j in range(0,Lsize):
                 ijk = i+j+k-1
                 if(ijk%2 == 0):
                     ia=ia+1
                     containts[ia][0] = i*xlat
                     containts[ia][1] =j*ylat
                     containts[ia][2] =(k-1)*bag+0.77
                     itype.append(1)
     return containts ,itype, ia
     			   		   

def filedumpc(filename,ia,containts,itype,lsize,strainx,strainy,lattice):
     Lsize = lsize
     strainx = strainx
     strainy=strainy
     bag = lattice/2
     xlat = bag*strainx
     txaxes = Lsize*bag*strainx
     tyaxes = Lsize*bag*strainy
     tzaxes = 80
     iop = 1
     with open(filename, "wt") as ft:
         m=0 
         ft.write("{0:5d}".format(ia))
         ft.write ("{0:2d}".format(iop))
         ft.write("{0:3d}".format(iop))
         ft.write('\n')
         ft.write ('Ni/Ni(100) growth multiatom diffusion')
         ft.write('\n')
         ft.write("{0:20.8f}".format(float(txaxes)))           
         ft.write("{0:20.8f}".format(float(tyaxes)))
         ft.write("{0:20.8f}".format(float(tzaxes)))
         ft.write('\n')
         ft.write('(3f12.6,i2)')
         ft.write('\n')
         for i in range(1,len(containts)):
            for j in range (3):
                 ft.write("{0:12.6f}".format(float(containts[i][j])))
            ft.write(str("{0:2d}".format(int(itype[m]))))
            m=m+1 
            ft.write('\n')

def filedumpj(filename,containts,ia):
    with open(filename, "wt") as f:
       f.write(str(ia))
       f.write('\n')
       for i in range(0,len(containts)):
            f.write('Ni')
            f.write('\t')
            for j in range(3):
                f.write(str(containts[i][j]))
                f.write('\t')
            f.write('\n')





