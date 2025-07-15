# =============================================================================
# 脚本功能：
#   检查粒子系统(Cascade)中所有使用的 StaticMesh 是否符合项目规范，包括：
#   1. StaticMesh 路径是否在指定目录下（root_path）。
#   2. StaticMesh 是否全部使用默认材质（default_material）。
#   检查不通过时会输出详细的警告日志，并返回 (bool, log_str)
# =============================================================================

import unreal
from unreal import (
    Material,
    ParticleSystem,
    ParticleEmitter,
    ParticleModuleTypeDataMesh,
    StaticMaterial,
    StaticMesh,
)

# input
particle_system: ParticleSystem
root_path: str
default_material: str
print_log: bool

# output
result: bool
log_str: str


default_mat: Material = unreal.EditorAssetLibrary.load_asset(default_material)

def is_mesh_path_valid(mesh_path: str, root_path: str, particl_path: str, lod_index: int, emitter_name: str, out_mesh: StaticMesh) -> tuple:
    """检查StaticMesh路径是否合规"""
    if not mesh_path.startswith(root_path):
        msg = f"""粒子StaticMesh路径不合规，必须使用{root_path}目录下的Mesh：
                粒子路径: {particl_path}
                LOD Level: {lod_index}
                Emitter: {emitter_name} 
                Mesh path: {out_mesh.get_path_name()}
            """
        return False, msg
    return True, ""

def reset_mesh_material_and_save(out_mesh: StaticMesh, idx: int,  mesh_path: str):
    """重置指定索引的材质并保存资产"""
    out_mesh.set_material(idx, default_mat)
    unreal.EditorAssetLibrary.save_asset(mesh_path)



def is_material_default(out_mesh: StaticMesh,mesh_path:str, default_material: str, particl_path: str, lod_index: int, emitter_name: str) -> tuple:
    """检查StaticMesh是否全部使用默认材质"""
    result = True
    log = ""
    materials: list[StaticMaterial] = out_mesh.static_materials
    
    for idx, mat in enumerate(materials):
        if mat.material_interface is None:
            reset_mesh_material_and_save(out_mesh, idx, mesh_path)
            # msg = f"""粒子StaticMesh材质异常，需要点击一下重置材质按钮：
            #         粒子路径: {particl_path}
            #         LOD Level: {lod_index}
            #         Emitter: {emitter_name} 
            #         Mesh path: {mesh_path} 
            #     """
            # log = msg
            continue
        
        mat_path = mat.material_interface.get_path_name()
        if mat_path != default_material:
            reset_mesh_material_and_save(out_mesh, idx, mesh_path)
            msg = f"""粒子StaticMesh必须使用默认材质，已自动重置材质: 
                    粒子路径: {particl_path}
                    LOD Level: {lod_index}
                    Emitter: {emitter_name} 
                    Mesh path: {mesh_path} 
                    Material: {mat_path}
                """
            # result = False
            log += msg + "\n"
    return result, log

def check_particle_mesh(particle_system: ParticleSystem, root_path: str, default_material: str, print_log: bool = True) -> tuple:
    """
    检查粒子系统中所有StaticMesh的路径和材质是否合规
    返回 (bool, log_str)
    """
    result = True
    log_str = ""
    particl_path = particle_system.get_path_name()
    lod_distances = particle_system.get_editor_property("lod_distances")
    lod_len = len(lod_distances)
    emitters: list[ParticleEmitter] = particle_system.get_cascade_system_emitters()

    for emitter in emitters:
        emitter_name = emitter.get_editor_property("emitter_name")
        for lod_index in range(lod_len):
            lod_level = emitter.get_cascade_emitter_lod_level(lod_index)
            if lod_level:
                type_data_module = lod_level.get_lod_level_type_data_module()
                if isinstance(type_data_module, ParticleModuleTypeDataMesh):
                    out_mesh: StaticMesh
                    out_mesh, *_ = (
                        type_data_module.get_particle_module_type_data_mesh_props()
                    )
                    if out_mesh:
                        mesh_path = out_mesh.get_path_name()
                        # 检查材质
                        ok, msg = is_material_default(out_mesh, mesh_path,default_material, particl_path, lod_index, emitter_name)
                        if not ok:
                            result = False
                            log_str += msg
                            if print_log and msg:
                                unreal.log_warning(msg)
                        # 检查路径
                        ok, msg = is_mesh_path_valid(mesh_path, root_path, particl_path, lod_index, emitter_name, out_mesh)
                        if not ok:
                            result = False
                            log_str += msg
                            if print_log and msg:
                                unreal.log_warning(msg)
    return result, log_str

# 调用
result, log_str = check_particle_mesh(particle_system, root_path, default_material, print_log)