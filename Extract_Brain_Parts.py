import nibabel as nib
import numpy as np
from skimage import measure
import os

# --- 配置路径 ---
# 假设你已经把 brain_work 剪切到了 Windows 桌面
input_file = r'C:\Users\miadi\OneDrive - PennO365\Desktop\Ding\Study\Models\brain_work\MyBrain_V1\mri\aseg.mgz'
output_dir = r'C:\Users\miadi\OneDrive - PennO365\Desktop\Ding\Study\Models\Brain_Parts_OBJ' 


# 核心标签对照表 (FreeSurfer Standard LUT)
# 你可以根据需要添加更多 ID
BRAIN_LABELS = {
    # 左侧深层核团
    10: "Left-Thalamus", 11: "Left-Caudate", 12: "Left-Putamen", 
    13: "Left-Pallidum", 17: "Left-Hippocampus", 18: "Left-Amygdala", 
    26: "Left-Accumbens-area", 28: "Left-VentralDC",
    # 右侧深层核团
    49: "Right-Thalamus", 50: "Right-Caudate", 51: "Right-Putamen", 
    52: "Right-Pallidum", 53: "Right-Hippocampus", 54: "Right-Amygdala", 
    58: "Right-Accumbens-area", 60: "Right-VentralDC",
    # 小脑与脑干
    7:  "Left-Cerebellum-White-Matter", 8: "Left-Cerebellum-Cortex",
    46: "Right-Cerebellum-White-Matter", 47: "Right-Cerebellum-Cortex",
    16: "Brain-Stem",
    # 胼胝体 (Corpus Callosum - 连接左右脑的桥梁)
    251: "CC_Posterior", 252: "CC_Mid_Posterior", 253: "CC_Central", 
    254: "CC_Mid_Anterior", 255: "CC_Anterior",
    # 脑室系统 (Ventricles)
    4:  "Left-Lateral-Ventricle", 43: "Right-Lateral-Ventricle",
    14: "3rd-Ventricle", 15: "4th-Ventricle",
    # 其他细微结构
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

    print(f"正在加载数据: {input_file} ...")
    img = nib.load(input_file)
    data = img.get_fdata()
    affine = img.affine  # 获取坐标变换矩阵

    for label_id, label_name in BRAIN_LABELS.items():
        print(f"正在提取: {label_name} (ID: {label_id})...")
        
        # 1. 创建二值掩码 (Binary Mask)
        binary_mask = np.where(data == label_id, 1, 0)
        
        if np.sum(binary_mask) == 0:
            print(f"跳过: {label_name} (未在数据中发现)")
            continue

        # 2. 运行 Marching Cubes 算法生成网格
        # level=0.5 是二值数据的标准阈值
        verts, faces, normals, values = measure.marching_cubes(binary_mask, level=0.5)

        # 3. 关键步：将体素坐标转换为实际的物理空间坐标 (RAS)
        # 这是为了确保所有零件最后能拼在一起
        # 这里的变换逻辑是 v_real = Affine * v_voxel
        verts_phys = np.c_[verts, np.ones(verts.shape[0])] @ affine.T
        verts_phys = verts_phys[:, :3]

        # 4. 保存为 OBJ
        obj_name = os.path.join(output_dir, f"{label_name}.obj")
        export_obj(verts_phys, faces, obj_name)

    print(f"\n--- [成功] ---")
    print(f"所有零件已保存至: {output_dir}")

if __name__ == "__main__":
    run_extraction()