import trimesh
import os
import glob

obj_dir = r'C:\Users\...\Brain_Parts_OBJ'
output_glb = r'C:\Users\...\Brain_Parts.glb'

def build_multicolor_smooth_brain():
    obj_files = glob.glob(os.path.join(obj_dir, "*.obj"))
    scene = trimesh.Scene()

    print(f"Found {len(obj_files)} parts. Starting colorful smoothing and packing...")

    for file_path in obj_files:
        part_name = os.path.basename(file_path).replace(".obj", "")
        mesh = trimesh.load(file_path)

        if isinstance(mesh, trimesh.Scene):
            mesh = mesh.dump(concatenate=True)

        # Apply Laplacian smoothing to reduce voxel staircase artifacts
        if mesh.vertices.shape[0] > 500:
            trimesh.smoothing.filter_laplacian(mesh, iterations=15)

        # --- COLOR LOGIC: assign each part a distinct color ---
        if "Cortex" in part_name:
            # Pial surface is kept white/light grey; transparency is applied in the HTML viewer
            mesh.visual.face_colors = [200, 200, 200, 255]
        else:
            # Generate a random unique color for each internal structure;
            # alpha is set to 255 (fully opaque) here — transparency is handled by the web shader
            mesh.visual.face_colors = trimesh.visual.color.random_color()

        scene.add_geometry(mesh, node_name=part_name)
        print(f"Processed with color: {part_name}")

    scene.export(output_glb)
    print(f"Final Colorful Smooth Brain saved to: {output_glb}")

if __name__ == "__main__":
    build_multicolor_smooth_brain()