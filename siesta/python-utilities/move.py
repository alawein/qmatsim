import os

def move_poscar_files():
   # Define paths and structures
   base_path = os.environ.get("QMATSIM_WORKSPACE_ROOT", "./materials")
   materials = ['MoS2', 'MoSe2', 'WS2', 'WSe2']
   supercells = {
       'MoS2': ['1x10', '1x20', '1x30'],
       'MoSe2': ['1x10', '1x20'],
       'WS2': ['1x10', '1x20'],
       'WSe2': ['1x10', '1x20']
   }

   for material in materials:
       print(f"\nProcessing {material}...")
       
       for supercell in supercells[material]:
           print(f"Processing {supercell}...")
           
           for strain in range(21):
               source = f"{base_path}/{material}/Monolayer/rectangular/{supercell}/{strain}/{material}.POSCAR"
               target = f"{base_path}/{material}/Monolayer/rectangular/{supercell}/{strain}/Structure/{material}.POSCAR"
               
               if os.path.exists(source):
                   try:
                       os.system(f"mv {source} {target}")
                       print(f"Moved {material} {supercell} strain {strain}")
                   except Exception as e:
                       print(f"Error moving {source}: {str(e)}")
               else:
                   print(f"File not found: {source}")

   print("\nMove operation completed!")

# Run the function
if __name__ == "__main__":
   move_poscar_files()
