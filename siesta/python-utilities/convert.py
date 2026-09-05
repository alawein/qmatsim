import os
import glob
from typing import List, Dict

def struct_to_poscar(filename: str, material: str) -> str:
    """Convert SIESTA STRUCT_IN to VASP POSCAR format."""
    # Dictionary for atomic numbers and symbols
    atomic_numbers = {
        '42': 'Mo',
        '74': 'W',
        '16': 'S',
        '34': 'Se'
    }
    
    # Read STRUCT_IN file
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Initialize POSCAR content
    poscar_lines = []
    
    # Add title
    poscar_lines.append(f"{material} structure\n")
    
    # Add scaling factor
    poscar_lines.append("1.0\n")
    
    # Add lattice vectors (first 3 lines stay the same)
    for i in range(3):
        poscar_lines.append(lines[i])
    
    # Create lists to store atoms by their actual species
    atoms_by_species = {}
    
    # Parse atoms and store them by their actual atomic number
    for line in lines[4:]:
        if not line.strip():
            continue
        parts = line.split()
        atomic_num = parts[1]  # This is the atomic number (e.g., 42 for Mo, 16 for S)
        coords = [float(parts[2]), float(parts[3]), float(parts[4])]
        
        if atomic_num not in atoms_by_species:
            atoms_by_species[atomic_num] = []
        atoms_by_species[atomic_num].append(coords)
    
    # Determine atom symbols and order from material name
    if material.startswith('Mo'):
        metal, metal_num = 'Mo', '42'
    else:
        metal, metal_num = 'W', '74'
    
    if material.endswith('S2'):
        nonmetal, nonmetal_num = 'S', '16'
    else:
        nonmetal, nonmetal_num = 'Se', '34'
    
    # Add atom type labels in correct order
    poscar_lines.append(f"{metal} {nonmetal}\n")
    
    # Add atom counts in correct order
    metal_atoms = atoms_by_species.get(metal_num, [])
    nonmetal_atoms = atoms_by_species.get(nonmetal_num, [])
    poscar_lines.append(f"{len(metal_atoms)} {len(nonmetal_atoms)}\n")
    
    # Add Direct coordinate label
    poscar_lines.append("Direct\n")
    
    # Add coordinates in correct order (metal atoms first, then non-metal)
    for coords in metal_atoms:
        poscar_lines.append(f"{coords[0]:.6f}  {coords[1]:.6f}  {coords[2]:.6f}\n")
    for coords in nonmetal_atoms:
        poscar_lines.append(f"{coords[0]:.6f}  {coords[1]:.6f}  {coords[2]:.6f}\n")
    
    return ''.join(poscar_lines)

def process_structure(base_path: str, material: str, structure_type: str, 
                     cell_type: str, supercell: str, strain: int) -> None:
    """
    Process a single structure configuration and convert to POSCAR.
    
    Args:
        base_path (str): Base directory path
        material (str): Material name
        structure_type (str): 'Bulk' or 'Monolayer'
        cell_type (str): 'primitive' or 'rectangular'
        supercell (str): Supercell size (e.g., '1x1', '1x10')
        strain (int): Strain percentage
    """
    struct_path = os.path.join(base_path, material, structure_type, 
                              cell_type, supercell, str(strain), "Structure")
    struct_file = os.path.join(struct_path, f"{material}.STRUCT_IN")
    poscar_file = os.path.join(struct_path, f"{material}.POSCAR")
    
    if os.path.exists(struct_file):
        try:
            # Convert and save POSCAR
            poscar_content = struct_to_poscar(struct_file, material)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(poscar_file), exist_ok=True)
            
            with open(poscar_file, 'w') as f:
                f.write(poscar_content)
            print(f"Converted {material} {structure_type} {cell_type} {supercell} strain {strain}")
        except Exception as e:
            print(f"Error processing {struct_file}: {str(e)}")
    else:
        print(f"File not found: {struct_file}")

def main():
    # Define paths and structures
    base_path = os.environ.get("QMATSIM_WORKSPACE_ROOT", "./materials")
    materials = ['MoS2', 'MoSe2', 'WS2', 'WSe2']
    structure_types = ['Bulk', 'Monolayer']
    cell_types = ['primitive', 'rectangular']
    supercells = ['1x1', '1x10', '10x1', '1x20', '20x1', '1x30', '30x1']
    
    # Process all combinations
    for material in materials:
        print(f"\nProcessing {material}...")
        for structure_type in structure_types:
            for cell_type in cell_types:
                # Determine which supercells to use based on material
                current_supercells = supercells
                if material != 'MoS2':
                    # For other materials, exclude 1x30 and 30x1
                    current_supercells = [sc for sc in supercells 
                                        if not ('30' in sc)]
                
                for supercell in current_supercells:
                    print(f"Processing {structure_type} {cell_type} {supercell}...")
                    for strain in range(21):  # 0 to 20% strain
                        process_structure(base_path, material, structure_type,
                                       cell_type, supercell, strain)
    
    print("\nConversion completed!")

if __name__ == "__main__":
    main()
