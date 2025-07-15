import unreal
from unreal import (
    BlendMode,
    Material,
    MaterialShadingModel,
    MaterialInstanceBasePropertyOverrides,
    MaterialInstanceConstant,
    ParticleModuleRequired,
    ParticleScreenAlignment,
    ParticleSystem,
    ParticleEmitter,
    MaterialInterface,
)

# input
particle_system: ParticleSystem
root_path: str
print_log: bool = True
# output
result: bool = True

ALLOWED_SCREEN_ALIGNMENT = ParticleScreenAlignment.PSA_RECTANGLE

particle_name = particle_system.get_name()
particl_path = particle_system.get_path_name()
lod_distances = particle_system.get_editor_property("lod_distances")
lod_len = len(lod_distances)

emitters: list[ParticleEmitter] = particle_system.get_cascade_system_emitters()


for emitter in emitters:
    # unreal.log(f"Processing Emitter: {emitter.get_name()}")
    for lod_index in range(lod_len):
        lod_level = emitter.get_cascade_emitter_lod_level(lod_index)
        if lod_level:
            required_module: ParticleModuleRequired = (
                lod_level.get_lod_level_required_module()
            )
            if required_module:
                screen_alignment: ParticleScreenAlignment
                material_interface, screen_alignment, *_ = (
                    required_module.get_particle_module_required_per_renderer_props()
                )
                if screen_alignment != ALLOWED_SCREEN_ALIGNMENT:
                    result = False
                    if print_log:
                        unreal.log_warning(
                            f"""粒子屏幕对齐(ScreenAlignment)方式不合规, 只能使用Rectangle方式:
                                粒子路径: {particl_path}
                                LOD Level: {lod_index}
                                Emitter: {emitter.get_name()}
                                ScreenAlignment: {screen_alignment}
                                """
                        )

