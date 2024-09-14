import os
from tqdm import tqdm

def rename_contcar_to_poscar():
    root_dir = "../GaN"
    
    # List all subdirectories in the root directory
    subdirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]
    
    # Initialize tqdm progress bar
    with tqdm(total=len(subdirs), desc="Progress", ncols=100) as pbar:
        for subdir in subdirs:
            # Path to the CONTCAR file in the current subdir
            contcar_path = os.path.join(root_dir, subdir, "CONTCAR")
            
            # Check if CONTCAR exists, then rename it to POSCAR
            if os.path.exists(contcar_path):
                os.rename(contcar_path, os.path.join(root_dir, subdir, "POSCAR"))
            
            # Update progress bar
            pbar.update(1)

if __name__ == "__main__":
    rename_contcar_to_poscar()
