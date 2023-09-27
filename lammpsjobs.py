import os
import shutil


# Define the folders
folders = [
    "V_TaV_C_2L",
    "V_TaV_C_2T",
    "V_TaV_C_3OP",
    "V_TaV_C_3IP",
    "V_TaV_C_4OP",
    "V_TaV_C_4IP",
    "V_TaV_C_5",
    "V_TaV_C_6",
    "AbBa",
    "Ab",
    "Ba",
    "VaBa",
    "VbAb",
    "V_TaV_C",
    "ISO_V_C",
    "ISO_V_Ta",
    "IB",
    "IA",
]


# Define the folder name
# folder_name = 'new_folder'

# Define the script as a string
script_template = '''#!/bin/bash
#SBATCH --constraint=intel
#SBATCH --partition=interactive
#SBATCH --job-name=JOB_NAME
#SBATCH --output=TaC.out
#SBATCH --error=TaC-%j.err
#SBATCH --time=0-02:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=48
#SBATCH --cpus-per-task=30
#SBATCH --mem-per-cpu=2
#SBATCH --mem=10GB
#SBATCH --export=ALL

#load modules with
module load python
module load gnu10
module load OneAPI/2022.1.2

srun /home/ikhatri/lammps-29Oct20/src/lmp_mpi < in.lammps > stdout
'''

# Define the LAMMPS script template
lammps_script_template = """
clear
units metal
atom_style atomic
boundary p p p
variable nx equal 5
variable ny equal 5
variable nz equal 5
    
read_data /scratch/ikhatri/LAMMPSCALCULATIONS/PINNTESTING/{folder}/TaC.RS.mini.dat

pair_style pinn
pair_coeff * * /scratch/ikhatri/PINN_POTENTIAL/Sep-20-2023/param_78/param.78.dat Ta C

{delete_group}

{delete_atoms}

thermo 5
thermo_style custom step pe lx ly lz vol press
neighbor 1 bin
neigh_modify delay 0 every 1 check yes
min_style cg

#fix 1 all box/relax aniso 0.0 vmax 0.001

minimize 1.0e-20 1.0e-20 80000 80000

variable natoms equal "count(all)"
variable PE0 equal "pe"
variable E0 equal "v_PE0/v_natoms"
variable L0 equal "lx"
variable L1 equal "ly"
variable L2 equal "lz"
variable avol equal "vol/v_natoms"
variable minpress equal "press"
variable a0 equal v_L0/v_nx
variable b0 equal v_L1/v_ny
variable c0 equal "v_L2/v_nz"
variable ca equal "v_c0/v_a0"

variable par_file string "params.txt"
shell echo ${{PE0}} ${{a0}} > ${{par_file}}

print "Total energy: ${{PE0}}"
print "Total atoms: ${{natoms}}"
print "Volume per atom: ${{avol}}"
print "Cohesive energy: ${{E0}} ${{natoms}} ${{minpress}} ${{a0}} ${{b0}} ${{c0}}"
write_dump all custom TaC.rocksalt.dat id type x y z
write_data TaC.defect.mini.dat
"""

output_dir = "/Users/indiraskhatri/Desktop/WorkSpace"

# Generate the LAMMPS script for each folder
for folder in folders:
    delete_group = ""
    delete_atoms = ""
    if folder == "ISO_V_Ta":
        delete_group = "group delatom id 648"
        delete_atoms = "delete_atoms group delatom compress no"
    elif folder == "ISO_V_C":
        delete_group = "group delatom id 400"
        delete_atoms = "delete_atoms group delatom compress no"
    elif folder == "V_TaV_C":
        delete_group = "group delatom id 400 600"
        delete_atoms = "delete_atoms group delatom compress no"
    elif folder == "AbBa":
        delete_group = "set atom 400 type 1\nset atom 648 type 2"
        delete_atoms = ""
    elif folder == "V_TaV_C_2L":
        delete_group = "group delatom id 400 600 650"
        delete_atoms = "delete_atoms group delatom compress no"
    elif folder == "V_TaV_C_2T":
        delete_group = "group delatom id 400 600 732"
        delete_atoms = "delete_atoms group delatom compress no"
    elif folder == "V_TaV_C_3OP":
        delete_group = "group delatom id 400 600 642 732"
        delete_atoms = "delete_atoms group delatom compress no"
    elif folder == "V_TaV_C_3IP":
        delete_group = "group delatom id 400 600 650 732"
        delete_atoms = "delete_atoms group delatom compress no"
    elif folder == "V_TaV_C_4OP":
        delete_group = "group delatom id 400 600 642 732 650"
        delete_atoms = "delete_atoms group delatom compress no"
    elif folder == "V_TaV_C_4IP":
        delete_group = "group delatom id 400 600 645 732 650"
        delete_atoms = "delete_atoms group delatom compress no"
    elif folder == "V_TaV_C_5":
        delete_group = "group delatom id 400 600 645 732 650 642"
        delete_atoms = "delete_atoms group delatom compress no"
    elif folder == "V_TaV_C_6":
        delete_group = "group delatom id 400 600 645 732 650 642 597"
        delete_atoms = "delete_atoms group delatom compress no"
    elif folder == "Ab":
        delete_group = "set atom 400 type 1"
        delete_atoms = ""
    elif folder == "Ba":
        delete_group = "set atom 648 type 2"
        delete_atoms = ""
    elif folder == "VaBa":
        delete_group = "set atom 733 type 2\ngroup delatom id 648"
        delete_atoms = "delete_atoms group delatom compress no"
    elif folder == "VbAb":
        delete_group = "set atom 732 type 1\ngroup delatom id 400"
        delete_atoms = "delete_atoms group delatom compress no"
    elif folder == "IA":
        delete_group = "create_atoms 1 single  10.076023545543642 10.076023545543642 19.03983518119453"
        delete_atoms = ""
    elif folder == "IB":
        delete_group = "create_atoms 2 single  10.076023545543642 10.076023545543642 19.03983518119453"
        delete_atoms = ""

    lammps_script = lammps_script_template.format(folder=folder, delete_group=delete_group, delete_atoms=delete_atoms)
    # Replace 'NameofJobs' with the folder name in the script
    updated_script = script_template.replace('JOB_NAME', folder)

    # Create a folder for the current script
    folder_path = os.path.join(output_dir, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    # Save the LAMMPS script inside the folder with the name "in.lammps"
    script_filename = os.path.join(folder_path, "jobscript")
    with open(script_filename, 'w') as file:
        file.write(updated_script)

    # Save the LAMMPS script template inside the folder with the name "in.lammps"
    lammps_filename = os.path.join(folder_path, "in.lammps")
    with open(lammps_filename, 'w') as file:
        file.write(lammps_script)

    print(f"Generated jobscript and in.lammps for folder: {folder}")
    os.chdir(folder_path)
    os.system('sbatch jobscript')
    os.chdir("../")