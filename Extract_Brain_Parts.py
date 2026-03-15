import nibabel as nib
import numpy as np
from skimage import measure
import os

# --- Configure paths ---
# Assumes brain_work has been moved to the Windows desktop
input_file = r'C:\Users\...\MyBrain_V1\mri\aseg.mgz'
output_dir = r'C:\Users\...\Brain_Parts_OBJ'


# Core label lookup table (FreeSurfer Standard LUT)
# Additional label IDs can be appended as needed
BRAIN_LABELS = {
    # Left-hemisphere deep nuclei
    10: "Left-Thalamus", 11: "Left-Caudate", 12: "Left-Putamen",
    13: "Left-Pallidum", 17: "Left-Hippocampus", 18: "Left-Amygdala",
    26: "Left-Accumbens-area", 28: "Left-VentralDC",
    # Right-hemisphere deep nuclei
    49: "Right-Thalamus", 50: "Right-Caudate", 51: "Right-Putamen",
    52: "Right-Pallidum", 53: "Right-Hippocampus", 54: "Right-Amygdala",
    58: "Right-Accumbens-area", 60: "Right-VentralDC",
    # Cerebellum and brainstem
    7:  "Left-Cerebellum-White-Matter", 8: "Left-Cerebellum-Cortex",
    46: "Right-Cerebellum-White-Matter", 47: "Right-Cerebellum-Cortex",
    16: "Brain-Stem",
    # Corpus Callosum (the commissural bridge connecting the two hemispheres)
    251: "CC_Posterior", 252: "CC_Mid_Posterior", 253: "CC_Central",
    254: "CC_Mid_Anterior", 255: "CC_Anterior",
    # Ventricular system
    4:  "Left-Lateral-Ventricle", 43: "Right-Lateral-Ventricle",
    14: "3rd-Ventricle", 15: "4th-Ventricle",
    # Other fine structures
    85: "Optic-Chiasm"
}

def export_obj(verts, faces, filename):
    with open(filename, 'w') as f:
        for v in verts:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            # OBJ indices are 1-based
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

def run_extraction():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Loading data: {input_file} ...")
    img = nib.load(input_file)
    data = img.get_fdata()
    affine = img.affine  # Retrieve the voxel-to-world coordinate transform matrix

    for label_id, label_name in BRAIN_LABELS.items():
        print(f"Extracting: {label_name} (ID: {label_id})...")

        # 1. Create a binary mask for the current label
        binary_mask = np.where(data == label_id, 1, 0)

        if np.sum(binary_mask) == 0:
            print(f"Skipping: {label_name} (not found in data)")
            continue

        # 2. Run Marching Cubes to generate a surface mesh
        # level=0.5 is the standard iso-surface threshold for binary data
        verts, faces, normals, values = measure.marching_cubes(binary_mask, level=0.5)

        # 3. Key step: transform voxel coordinates into physical RAS space
        # This ensures all parts can be correctly reassembled in world space.
        # The transform is: v_real = Affine * v_voxel
        verts_phys = np.c_[verts, np.ones(verts.shape[0])] @ affine.T
        verts_phys = verts_phys[:, :3]

        # 4. Save as OBJ
        obj_name = os.path.join(output_dir, f"{label_name}.obj")
        export_obj(verts_phys, faces, obj_name)

    print(f"\n--- [Done] ---")
    print(f"All parts saved to: {output_dir}")

if __name__ == "__main__":
    run_extraction()