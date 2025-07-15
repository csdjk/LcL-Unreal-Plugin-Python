# =============================================================================
# 需要安装的插件：
#   1. Cascade To Niagara Converter
# 脚本功能：
#   检查粒子（Cascade）系统中所有使用的材质是否符合项目规范，包括：
#   1. 粒子材质必须为 Material Instance，不能直接使用 Material。
#   2. 粒子材质母材质路径必须在指定目录下（root_path）。
#   3. 粒子材质的 ShadingModel 必须为 Unlit。
#   4. 粒子材质的 BlendMode 只能为 Opaque、Translucent 或 Additive。
#   检查不通过时会输出详细的警告日志，并返回 (bool, log_str)
# =============================================================================

import unreal
from unreal import (
    BlendMode,
    Material,
    MaterialShadingModel,
    MaterialInstanceBasePropertyOverrides,
    MaterialInstanceConstant,
    ParticleModuleRequired,
    ParticleSystem,
    ParticleEmitter,
    MaterialInterface,
)

# input
particle_system: ParticleSystem
root_path: str
print_log: bool

# output
result: bool = True
log_str: str = ""

ALLOWED_BLEND_MODES = [
    BlendMode.BLEND_OPAQUE,
    BlendMode.BLEND_TRANSLUCENT,
    BlendMode.BLEND_ADDITIVE,
]

ALLOWED_SHADING_MODEL = MaterialShadingModel.MSM_UNLIT

def is_shader_path_valid(shader_path: str, root_path: str) -> bool:
    """检查shader路径是否在指定根目录下"""
    return shader_path.startswith(root_path)

def check_shader_path(material_interface: MaterialInterface, root_path: str, particle_name: str, lod_index: int, emitter_name: str) -> tuple:
    """检查母材质路径是否合法"""
    shader: Material = material_interface.get_base_material()
    shader_path = shader.get_path_name()
    if not is_shader_path_valid(shader_path, root_path):
        log = f"""粒子Shader路径不合规, 只能使用{root_path}路径下的Shader:
                粒子: {particle_name} 
                LOD Level: {lod_index}
                Emitter: {emitter_name} 
                Shader path: {shader_path}
            """
        return False, log
    return True, ""

def check_material_properties(material_interface: MaterialInterface, particl_path: str, lod_index: int, emitter_name: str) -> tuple:
    """检查材质属性是否合法"""
    material_path = material_interface.get_path_name()
    material_instance: MaterialInstanceConstant = unreal.load_asset(material_path)
    base_property_overrides: MaterialInstanceBasePropertyOverrides = (
        material_instance.get_editor_property("base_property_overrides")
    )
    result = True
    log = ""

    shading_mode = base_property_overrides.get_editor_property("shading_model")
    if shading_mode != ALLOWED_SHADING_MODEL:
        log += f"""粒子材质的 ShadingModel 不合规,只能使用Unlit:
                粒子路径: {particl_path} 
                LOD Level: {lod_index}
                Emitter: {emitter_name}
                Material: {material_path}
                ShadingModel: {shading_mode}
            \n"""
        result = False

    blend_mode: BlendMode = base_property_overrides.get_editor_property("blend_mode")
    if blend_mode not in ALLOWED_BLEND_MODES:
        log += f"""粒子材质 BlendMode 不合规,只能使用Opaque、Translucent、Additive三种模式:
                粒子路径: {particl_path} 
                LOD Level: {lod_index}
                Emitter: {emitter_name}
                Material: {material_path} 
                BlendMode: {blend_mode}
            \n"""
        result = False

    return result, log

def check_particle_materials(particle_system: ParticleSystem, root_path: str, print_log: bool = True) -> tuple:
    """主检查函数，返回 (bool, log_str)"""
    result = True
    log_str = ""
    particle_name = particle_system.get_name()
    particl_path = particle_system.get_path_name()
    lod_distances = particle_system.get_editor_property("lod_distances")
    lod_len = len(lod_distances)
    emitters: list[ParticleEmitter] = particle_system.get_cascade_system_emitters()

    for emitter in emitters:
        emitter_name = emitter.get_editor_property("emitter_name")
        
        for lod_index in range(lod_len):
            lod_level = emitter.get_cascade_emitter_lod_level(lod_index)
            if lod_level:
                required_module: ParticleModuleRequired = (
                    lod_level.get_lod_level_required_module()
                )
                if required_module:
                    material_interface, *_ = (
                        required_module.get_particle_module_required_per_renderer_props()
                    )
                    # 检查是否为MaterialInstance
                    if isinstance(material_interface, Material):
                        msg = f"""粒子材质必须使用Material Instance:
                                粒子路径: {particl_path}
                                LOD Level: {lod_index}
                                Emitter: {emitter_name}
                             """
                        if print_log:
                            unreal.log_warning(msg)
                        # log_str += msg + "\n"
                        log_str = msg
                        result = False
                        continue

                    if isinstance(material_interface, MaterialInterface):
                        # 检查Shader路径
                        ok, msg = check_shader_path(material_interface, root_path, particle_name, lod_index, emitter_name)
                        if not ok:
                            if print_log:
                                unreal.log_warning(msg)
                            # log_str += msg + "\n"
                            log_str = msg
                            result = False
                        # 检查材质属性
                        ok, msg = check_material_properties(material_interface, particl_path, lod_index, emitter_name)
                        if not ok:
                            if print_log:
                                unreal.log_warning(msg)
                            # log_str += msg + "\n"
                            log_str = msg
                            result = False
    return result, log_str

result, log_str = check_particle_materials(particle_system, root_path, print_log)