import trimesh
import os
import glob

obj_dir = r'C:\Users\miadi\OneDrive - PennO365\Desktop\Ding\Study\Models\Brain_Parts_OBJ'
output_glb = r'C:\Users\miadi\OneDrive - PennO365\Desktop\Ding\Study\Models\Brain_Parts.glb'

def build_multicolor_smooth_brain():
    obj_files = glob.glob(os.path.join(obj_dir, "*.obj"))
    scene = trimesh.Scene()

    print(f"Found {len(obj_files)} parts. Starting colorful smoothing and packing...")

    for file_path in obj_files:
        part_name = os.path.basename(file_path).replace(".obj", "")
        mesh = trimesh.load(file_path)
        
        if isinstance(mesh, trimesh.Scene):
            mesh = mesh.dump(concatenate=True)

        # Apply Laplacian Smoothing (same as before)
        if mesh.vertices.shape[0] > 500:
            trimesh.smoothing.filter_laplacian(mesh, iterations=15)
        
        # --- COLOR LOGIC: Give each part a distinct color ---
        if "Cortex" in part_name:
            # Pial Surface is kept white/light grey, and we make it transparent in HTML
            mesh.visual.face_colors = [200, 200, 200, 255]
        else:
            # Use trimesh to generate a random unique color for internal parts
            # The transparency is handled here by 255 (fully opaque)
            mesh.visual.face_colors = trimesh.visual.color.random_color()
        
        scene.add_geometry(mesh, node_name=part_name)
        print(f"Processed with color: {part_name}")

    scene.export(output_glb)
    print(f"Final Colorful Smooth Brain saved to: {output_glb}")

if __name__ == "__main__":
    build_multicolor_smooth_brain()
