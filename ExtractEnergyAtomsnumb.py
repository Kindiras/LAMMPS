import os

root_directory = "/scratch/ikhatri/LAMMPSCALCULATIONS/PINNTESTING/defects/5by5by5/"
data = []
folder_names = ["AbBa", "Ba", "V_TaV_C", "Relax", "Ab", "V_TaV_C_2L", "V_TaV_C_3IP", "V_TaV_C_3OP", "V_TaV_C_4IP", "V_TaV_C_4OP", "V_TaV_C_5", "V_TaV_C_6", "ISO_V_C", "ISO_V_Ta", "V_TaV_C_2T", "IA", "IB", "VbAb", "VaBa"]

for folder_name in folder_names:
    folder_path = os.path.join(root_directory, folder_name)
    
    # Check if params.txt exists in the current folder
    params_file_path = os.path.join(folder_path, "params.txt")
    tac_defect_file_path = os.path.join(folder_path, "TaC.defect.mini.dat")
    
    if os.path.exists(params_file_path):
        print("Folder has params.txt:", folder_name)
        with open(params_file_path, "r") as params_file:
            first_line = params_file.readline().strip().split()
            
            if first_line:
                data.append([folder_name, first_line[0]])
                print("Energy:", first_line[0])

    if os.path.exists(tac_defect_file_path):
        with open(tac_defect_file_path, "r") as tac_defect_file:
            lines = tac_defect_file.readlines()
            if len(lines) >= 3:
                third_line_parts = lines[2].strip().split()
                if len(third_line_parts) >= 1:
                    data[-1].append(third_line_parts[0])
                    print("numbatoms:",third_line_parts[0])
                    print("Value from TaC.defect.mini.dat:", third_line_parts[0])
        
    else:
        print("This folder does not have params.txt", folder_name)
        # If params.txt doesn't exist, check for subfolders
        subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
        print(subfolders)
        
        if subfolders:
            # If there are subfolders, look for a subfolder named "energy"
            if "energy" in subfolders:
                energy_folder_path = os.path.join(folder_path, "energy")
                params_file_path = os.path.join(energy_folder_path, "params.txt")
                
                if os.path.exists(params_file_path):
                    with open(params_file_path, "r") as params_file:
                        first_line = params_file.readline().strip().split()
                        
                        if first_line:
                            data.append([folder_name, first_line[0]])
                            print("Energy:", first_line[0])
                
                # Read TaC.defect.mini.dat and store data from the third line's first element
                tac_defect_file_path = os.path.join(energy_folder_path, "TaC.defect.mini.dat")
                if os.path.exists(tac_defect_file_path):
                    with open(tac_defect_file_path, "r") as tac_defect_file:
                        lines = tac_defect_file.readlines()
                        if len(lines) >= 3:
                            third_line_parts = lines[2].strip().split()
                            if len(third_line_parts) >= 1:
                                data[-1].append(third_line_parts[0])
                                print("numbatoms:",third_line_parts[0])
                                print("Value from TaC.defect.mini.dat:", third_line_parts[0])

with open("check.txt", "w") as output_file:
    for item in data:
        if len(item) >= 3:
            output_file.write(f"{item[0]}\t{item[1]}\t{item[2]}\n")

print("Data saved to check.txt")