import trimesh
import os
import glob

# --- 配置路径 ---
obj_dir = r'C:\Users\miadi\OneDrive - PennO365\Desktop\Ding\Study\Models\Brain_Parts_OBJ'
output_glb = r'C:\Users\miadi\OneDrive - PennO365\Desktop\Ding\Study\Models\Brain_Parts.glb'

def build_smooth_brain():
    obj_files = glob.glob(os.path.join(obj_dir, "*.obj"))
    scene = trimesh.Scene()

    print(f"Found {len(obj_files)} parts. Starting smoothing and packing...")

    for file_path in obj_files:
        part_name = os.path.basename(file_path).replace(".obj", "")
        mesh = trimesh.load(file_path)
        
        if isinstance(mesh, trimesh.Scene):
            mesh = mesh.dump(concatenate=True)

        # --- 核心：拉普拉斯平滑算法 ---
        # 针对皮层和小脑等大型结构进行 15 次迭代，消除 Voxel 锯齿
        if mesh.vertices.shape[0] > 500:
            trimesh.smoothing.filter_laplacian(mesh, iterations=15)
        
        # 给不同部位打上颜色标签（方便 Three.js 识别）
        if "Cortex" in part_name:
            # 给皮层设置一个基础色，HTML 里会把它变透明
            mesh.visual.face_colors = [200, 200, 255, 100]
        
        scene.add_geometry(mesh, node_name=part_name)
        print(f"Refined: {part_name}")

    # 导出为二进制 GLB
    scene.export(output_glb)
    print(f"\n--- [COMPLETED] ---")
    print(f"Smooth Brain saved to: {output_glb}")

if __name__ == "__main__":
    build_smooth_brain()