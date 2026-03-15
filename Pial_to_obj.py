import nibabel as nib
import trimesh
import os

# Set your paths
surf_dir = r'C:\Users\miadi\OneDrive - PennO365\Desktop\Ding\Study\Models\brain_work\MyBrain_V1\surf' 
output_dir = r'C:\Users\miadi\OneDrive - PennO365\Desktop\Ding\Study\Models\Brain_Parts_OBJ'

def convert_pial_t1(side):
    # 直接锁定你提到的 .pial.T1 格式
    pial_path = os.path.join(surf_dir, f'{side}.pial.T1')
    
    if not os.path.exists(pial_path):
        print(f"Error: File not found: {pial_path}")
        return

    print(f"Processing {side} hemisphere surface...")
    
    try:
        # 使用 nibabel 读取 FreeSurfer 几何数据
        coords, faces = nib.freesurfer.read_geometry(pial_path)
        
        # 创建 3D 网格对象
        mesh = trimesh.Trimesh(vertices=coords, faces=faces)
        
        # 导出为 OBJ，存放到你的零件文件夹
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