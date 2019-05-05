# LAMMPS
This is LAMMPS input script to deposit Cd atoms on Cd-terminated CdTe zincblend structure. 

units metal
processors 2 2 2
atom_style bond
dimension 3
boundary p p f

read_data ~/lammps/events/Te-terminated/Tedim1eV10a300K

group adatoms type 3

bond_style none 

pair_style bop save
pair_coeff * * /usr/local/src/lammps/lammps-16Mar18-intelmpi/potentials/CdTe.bop.table Te Cd Cd 
comm_modify cutoff 14.70

region bfix block 0 68.3 0 68.3 0 5.5 units lattice
group bfix region bfix

region isotherm block 0 68.3 0 68.3 5.5 12.7 units lattice
group isotherm region isotherm

region free block 0 68.3 0 68.3 12.7 23.5 units lattice
group free region free

region mobile block 0 68.3 0 68.3 5.464 23.5 units lattice
group mobile region mobile

region slab block 0 64.9 0 64.9 28.2 28.2 units lattice

compute	 add mobile temp
compute ke adatoms ke/atom
compute pe adatoms pe/atom
compute_modify	add dynamic/dof yes extra/dof 0
compute_modify  ke dynamic/dof yes extra/dof 0
compute_modify  pe dynamic/dof yes extra/dof 0

neighbor 2.0 bin
neigh_modify delay 0 every 1 check yes
timestep 0.001

velocity mobile create 300.0 49284522
fix 1 bfix setforce 0.0 0.0 0.0
fix 2 isotherm temp/berendsen 300 300 0.001
fix 3 mobile nve 
fix 4 adatoms nve          
fix 5 adatoms deposit 1 0 1 1234535 region slab vz -12.3 -12.3 units lattice 
thermo_style custom step time atoms temp epair etotal ke pe
thermo 50

thermo_modify lost warn flush yes temp add
dump depo all custom 10 dump.Tedim1eV300k10a id type x y z vx vy vz
#dump eng adatoms custom 50 dump.Energy id type x y z vx vy vz c_ke c_pe
run 10000
write_data Tedim1eV_depo_300k10a.dat
