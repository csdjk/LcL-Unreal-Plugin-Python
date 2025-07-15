import unreal
from unreal import (
    MaterialInstanceConstant
)

# input
material_instance: MaterialInstanceConstant
material_path0: str
material_path1: str

# output
result: bool = True
log_str: str = ""


def is_shader_path_valid(shader_path: str, path0: str, path1: str) -> bool:
    """判断shader路径是否不在指定的两个目录下"""
    return (shader_path.startswith(path0) or shader_path.startswith(path1))

def check_material_instance_shader_path(material_instance: MaterialInstanceConstant, path0: str, path1: str) -> tuple:
    """
    检查材质实例的母材质路径是否在path0和path1以外
    :param material_instance: 材质实例
    :param path0: 允许的目录0
    :param path1: 允许的目录1
    :return: (bool, log_str) - True为合规，False为不合规
    """
    if not material_instance:
        return False, "未传入有效的材质实例"
    base_material = material_instance.get_base_material()
    shader_path = base_material.get_path_name()
    if not is_shader_path_valid(shader_path, path0, path1):
        log_str = f"角色材质实例 {material_instance.get_name()} 的Shader只能使用 {path0} 或 {path1} 下的"
        return False, log_str
    return True, ""


result, log_str = check_material_instance_shader_path(material_instance, material_path0, material_path1)