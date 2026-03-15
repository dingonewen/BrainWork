import nibabel as nib
import trimesh
import os

# Set your paths
surf_dir = r'C:\Users\...\MyBrain_V1\surf'
output_dir = r'C:\Users\...\Brain_Parts_OBJ'

def convert_pial_t1(side):
    # Directly target the .pial.T1 surface format
    pial_path = os.path.join(surf_dir, f'{side}.pial.T1')

    if not os.path.exists(pial_path):
        print(f"Error: File not found: {pial_path}")
        return

    print(f"Processing {side} hemisphere surface...")

    try:
        # Read FreeSurfer surface geometry using nibabel
        coords, faces = nib.freesurfer.read_geometry(pial_path)

        # Create a 3D mesh object
        mesh = trimesh.Trimesh(vertices=coords, faces=faces)

        # Export as OBJ into the parts output folder
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_path = os.path.join(output_dir, f'{side}_Cortex.obj')
        mesh.export(output_path)
        print(f"Success! Created: {output_path}")
    except Exception as e:
        print(f"Failed to convert {side}: {e}")

if __name__ == "__main__":
    convert_pial_t1('lh')
    convert_pial_t1('rh')