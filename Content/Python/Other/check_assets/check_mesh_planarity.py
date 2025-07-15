import unreal
from unreal import (
    StaticMesh,
)
from collections import defaultdict

# input
static_mesh: StaticMesh
edge_max: int
face_count_max: int
print_log: bool
# output
result: bool
log_str: str


mesh_path = static_mesh.get_path_name()

    

def are_normals_aligned(normals, tolerance=1e-4):
    """判断所有法线是否一致（即mesh是否为平面）"""
    if not normals:
        return False
    ref = normals[0]
    for n in normals[1:]:
        if (ref - n).length() > tolerance:
            return False
    return True

def is_colinear(p1, p2, p3, tolerance=1e-4):
    """判断三点是否共线"""
    v1 = unreal.Vector(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
    v2 = unreal.Vector(p3.x - p2.x, p3.y - p2.y, p3.z - p2.z)
    cross = v1.cross(v2)
    colinear = cross.length() < tolerance
    # unreal.log_warning(f"共线判断: {p1}, {p2}, {p3} -> {colinear} (cross.length={cross.length()})")
    return colinear

def count_polygon_edges_by_merging(vertices, boundary_edges, tolerance=1e-4):
    """
    统计多边形边数（合并共线边），输入为顶点列表和边界边集合
    1. 构建边界点的邻接表
    2. 顺序遍历边界点，形成有序边界点序列
    3. 遍历有序点序列，合并共线边，统计真实边数
    """
    edge_map = defaultdict(list)
    for a, b in boundary_edges:
        edge_map[a].append(b)
        edge_map[b].append(a)
    start = next(iter(edge_map))  # 任取一个边界点作为起点
    ordered = [start]
    prev = None
    curr = start
    # 顺序遍历边界点，形成闭环
    while True:
        next_points = [p for p in edge_map[curr] if p != prev]
        if not next_points:
            break
        next_pt = next_points[0]
        ordered.append(next_pt)
        prev, curr = curr, next_pt
        if curr == start:
            break
    # 如果首尾重复，去掉最后一个
    if ordered[0] == ordered[-1]:
        ordered = ordered[:-1]

    # 合并共线边，统计真实边数
    count = 0
    n = len(ordered)
    for i in range(n):
        p1 = vertices[ordered[i - 1]]
        p2 = vertices[ordered[i]]
        p3 = vertices[ordered[(i + 1) % n]]
        if not is_colinear(p1, p2, p3, tolerance):
            count += 1
    # unreal.log_warning(f"合并共线后边数: {count}")
    return count

def get_polygon_edge_count(vertices, triangles, tolerance=1e-4):
    """
    统计平面mesh的多边形边数，排除有洞的情况
    """
    edge_count = defaultdict(int)
    for i in range(0, len(triangles), 3):
        idx0, idx1, idx2 = triangles[i], triangles[i+1], triangles[i+2]
        edges = [
            tuple(sorted((idx0, idx1))),
            tuple(sorted((idx1, idx2))),
            tuple(sorted((idx2, idx0))),
        ]
        for edge in edges:
            edge_count[edge] += 1
    boundary_edges = [edge for edge, count in edge_count.items() if count == 1]
    if not boundary_edges:
        return 0

    # 统计边界环数量
    edge_map = defaultdict(list)
    for a, b in boundary_edges:
        edge_map[a].append(b)
        edge_map[b].append(a)
    visited = set()
    rings = 0
    for start in edge_map:
        if start in visited:
            continue
        rings += 1
        curr = start
        prev = None
        while True:
            visited.add(curr)
            next_points = [p for p in edge_map[curr] if p != prev and p not in visited]
            if not next_points:
                break
            next_pt = next_points[0]
            prev, curr = curr, next_pt
            if curr == start:
                break
    if rings > 1:
        # 有多个环，说明有洞，直接返回0
        return 0

    # 只有一个环，正常统计边数
    count = count_polygon_edges_by_merging(vertices, boundary_edges, tolerance)
    return count


def check_mesh_planarity(static_mesh: StaticMesh,edge_max:int, face_count_max: int, print_log: bool = True) -> tuple:
        
    section_count = static_mesh.get_num_sections(0)

    for section_index in range(section_count):
        vertices, triangles, normals, uvs, tangents = unreal.ProceduralMeshLibrary.get_section_from_static_mesh(static_mesh, 0, section_index)
        # 判断是否共面
        if are_normals_aligned(normals):
            polygon_edge_count = get_polygon_edge_count(vertices, triangles)
            # polygon_edge_count = 0 代表有洞，排除掉
            if polygon_edge_count > 2 and polygon_edge_count <= edge_max:
                face_count = len(triangles) // 3
                if face_count > face_count_max:
                    log_str = f"""特效的平面Mesh的面数超过最大限制(最大{face_count_max}):
                                Mesh路径: {mesh_path}
                                section_index: {section_index}
                                识别的边数: {polygon_edge_count}
                                三角面数: {face_count}
                            """
                    if print_log:
                        unreal.log_warning(log_str)
                    return (False,log_str)
    
    return (True,  "")
            

result,log_str = check_mesh_planarity(static_mesh,edge_max, face_count_max, print_log)