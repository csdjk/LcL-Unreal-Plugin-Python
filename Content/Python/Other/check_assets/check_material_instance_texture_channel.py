import unreal
import math
from typing import List, Tuple

def check_mesh_face_orientation():
    """检测当前选中的静态网格体中的三角面朝向是否一致"""
    
    # 获取当前编辑器选中的静态网格体
    selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    static_meshes = [asset for asset in selected_assets if isinstance(asset, unreal.StaticMesh)]
    
    if not static_meshes:
        unreal.log_warning("请选择一个静态网格体！")
        return False
    
    static_mesh = static_meshes[0]
    unreal.log(f"正在检查 {static_mesh.get_name()} 的面朝向")
    
    # 获取LOD和Section信息
    lod_count = static_mesh.get_num_lods()
    if lod_count == 0:
        unreal.log_error("网格体没有LOD数据")
        return False
    
    # 我们使用LOD 0
    lod_index = 0
    section_count = static_mesh.get_num_sections(lod_index)
    
    if section_count == 0:
        unreal.log_error(f"LOD {lod_index} 没有任何Section")
        return False
    
    # 用于存储所有三角面法线
    all_face_normals: List[unreal.Vector] = []
    
    # 遍历所有Section
    for section_index in range(section_count):
        # 使用提供的API获取几何数据
        vertices, triangles, normals, uvs, tangents = unreal.ProceduralMeshLibrary.get_section_from_static_mesh(
            static_mesh, lod_index, section_index
        )
        
        # 计算每个三角面的法线
        for i in range(0, len(triangles), 3):
            if i + 2 >= len(triangles):
                break
                
            # 获取三角形的三个顶点索引
            idx1, idx2, idx3 = triangles[i], triangles[i+1], triangles[i+2]
            
            # 获取三角形的三个顶点法线
            n1, n2, n3 = normals[idx1], normals[idx2], normals[idx3]
            
            # 计算三角形的平均法线
            avg_normal = unreal.Vector(
                (n1.x + n2.x + n3.x) / 3.0,
                (n1.y + n2.y + n3.y) / 3.0,
                (n1.z + n2.z + n3.z) / 3.0
            )
            
            # 确保法线是单位向量
            avg_normal.normalize()
            all_face_normals.append(avg_normal)
    
    # 检查所有法线是否指向相似方向
    if not all_face_normals:
        unreal.log_error("无法计算法线")
        return False
        
    reference_normal = all_face_normals[0]
    inconsistent_count = 0
    
    # 检查每个法线与参考法线的夹角是否小于阈值
    angle_threshold = 1.0  # 90度阈值，可以根据需要调整
    cos_threshold = math.cos(math.radians(angle_threshold))
    
    for normal in all_face_normals[1:]:
        dot_product = reference_normal.x * normal.x + reference_normal.y * normal.y + reference_normal.z * normal.z
        
        # 如果点积为负，表示法线方向相反(夹角>90度)
        if dot_product < cos_threshold:
            inconsistent_count += 1
    
    consistent = inconsistent_count == 0
    
    if consistent:
        unreal.log(f"所有三角面朝向一致")
    else:
        unreal.log_warning(f"检测到 {inconsistent_count} 个不一致的面朝向，总面数: {len(all_face_normals)}")
    
    return consistent

def visualize_inconsistent_faces():
    """可视化不一致的面朝向（通过绘制调试线）"""
    # 这部分代码可以扩展实现，在编辑器中可视化显示不一致的面
    pass

# 执行检查
check_mesh_face_orientation()