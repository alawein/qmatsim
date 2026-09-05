import os
import numpy as np
from datetime import datetime

# List of supercells
supercells = ['1x10', '1x20', '1x30']

def process_struct_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Process lattice vectors
    new_lines = []
    for i in range(3):
        coords = [float(x) for x in lines[i].split()]
        new_lines.append(f"{coords[0]:.3f} {coords[1]:.3f} {coords[2]:.3f}\n")
    
    # Add number of atoms
    new_lines.append(lines[3])  # Keep the original "60" line
    
    # Process atomic coordinates
    for line in lines[4:]:
        if not line.strip():
            continue
        parts = line.split()
        type_prefix = f"{parts[0]} {parts[1]}"
        coords = [float(parts[2]), float(parts[3]), float(parts[4])]
        new_lines.append(f"{type_prefix} {coords[0]:.3f} {coords[1]:.3f} {coords[2]:.3f}\n")
    
    # Write back to file
    with open(filename, 'w') as f:
        f.writelines(new_lines)

# Create backup timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

for supercell in supercells:
    print(f"\nProcessing MoS2 {supercell}...")
    
    # Create backup directory for this supercell
    backup_dir = f"{os.environ.get('QMATSIM_BACKUP_ROOT', './backups')}/MoS2_{supercell}_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)

    base_path = f"{os.environ.get('QMATSIM_WORKSPACE_ROOT', '.')}/siesta/materials/MoS2/Monolayer/rectangular/{supercell}"
    
    # Backup and process for each strain
    for strain in range(21):
        strain_path = f"{base_path}/{strain}"
        struct_path = f"{strain_path}/Structure/MoS2.STRUCT_IN"
        
        if os.path.exists(struct_path):
            # Create backup
            backup_path = f"{backup_dir}/{strain}/Structure"
            os.makedirs(backup_path, exist_ok=True)
            os.system(f"cp {struct_path} {backup_path}/")
            print(f"Backed up {supercell} strain {strain}")
            
            # Process file
            process_struct_file(struct_path)
            print(f"Processed {supercell} strain {strain}")
            
            # Copy to STRUCT_IN and STRUCT_OUT
            os.system(f"cp {struct_path} {strain_path}/MoS2.STRUCT_IN")
            os.system(f"cp {struct_path} {strain_path}/MoS2.STRUCT_OUT")
            print(f"Copied files for {supercell} strain {strain}")

print("\nAll supercells processed!")
print(f"Backups stored in {os.environ.get('QMATSIM_BACKUP_ROOT', './backups')}/*_{timestamp}")
