import unreal
import os
import math

MATERIAL_DIR = "/Game/Art/Maps/Standard/Material_Validation/Materials"
SPACING = 1000.0
BLOCK_SPACING = 4500.0  # 文件夹分块间距
SPHERE_HEIGHT = 100.0
TEXT_HEIGHT = 300.0
BLOCK_TITLE_HEIGHT = 800.0   # block标题高度
TEXT_SIZE = 100.0
BLOCK_TITLE_SIZE = 200.0     # block标题字体大小
FOLDER_NAME = "material"
SPHERE_MESH_PATH = '/Engine/BasicShapes/Sphere'
BOARD_MATERIAL_PATH = "/Game/Art/Maps/Standard/Material_Validation/Materials/ChessBoard/MI_WhiteBox_Constants"

def get_best_grid(n):
    x = math.ceil(math.sqrt(n))
    y = math.ceil(n / x)
    return x, y


def get_color_by_index(idx, total):
    """根据索引生成不同的颜色（RGB 0-1）"""
    hue = (idx / total) % 1.0
    color = unreal.LinearColor()
    color.set_random_hue()
    return color.to_rgbe()

def create_spheres_for_materials():
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    assets = asset_registry.get_assets_by_path(MATERIAL_DIR, recursive=True)

    # 按文件夹分组
    folder_dict = {}
    for asset in assets:
        asset: unreal.AssetData
        folder_name = os.path.basename(str(asset.package_path))
        if folder_name not in folder_dict:
            folder_dict[folder_name] = []
        folder_dict[folder_name].append((str(asset.package_name), folder_name, str(asset.asset_name)))

    sphere_mesh = unreal.EditorAssetLibrary.load_asset(SPHERE_MESH_PATH)
    box_mesh = unreal.EditorAssetLibrary.load_asset('/Engine/BasicShapes/Cube')
    board_material = unreal.EditorAssetLibrary.load_asset(BOARD_MATERIAL_PATH)

    # block grid 计算
    block_names = list(folder_dict.keys())
    block_count = len(block_names)
    block_cols, block_rows = get_best_grid(block_count)

    # 计算每个block的宽高
    block_sizes = []
    for mats in folder_dict.values():
        cols, rows = get_best_grid(len(mats))
        width = (cols - 1) * SPACING if cols > 1 else 0
        height = (rows - 1) * SPACING if rows > 1 else 0
        block_sizes.append((width, height, cols, rows))

    # block grid整体居中
    total_grid_width = block_cols * BLOCK_SPACING
    total_grid_height = block_rows * BLOCK_SPACING
    start_x = -total_grid_width / 2 + BLOCK_SPACING / 2
    start_y = -total_grid_height / 2 + BLOCK_SPACING / 2

    for block_idx, folder in enumerate(block_names):
        mats = folder_dict[folder]
        block_width, block_height, cols, rows = block_sizes[block_idx]
        grid_row = block_idx // block_cols
        grid_col = block_idx % block_cols

        # block左上角坐标
        block_origin_x = start_x + grid_col * BLOCK_SPACING - block_width / 2
        block_origin_y = start_y + grid_row * BLOCK_SPACING - block_height / 2

        folder_path = f"{FOLDER_NAME}/{folder}" if folder else FOLDER_NAME

        # 生成block大标题（放到folder目录下）
        block_title_location = unreal.Vector(
            block_origin_x + block_width / 2,
            block_origin_y - SPACING,
            BLOCK_TITLE_HEIGHT
        )
        block_title_actor:unreal.TextRenderActor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.TextRenderActor,
            block_title_location
        )
        block_title_actor.set_actor_label(f"BlockTitle_{folder}")
        block_title_actor.set_folder_path(folder_path)
        block_title_comp = block_title_actor.text_render
        block_title_comp.set_text(folder)
        block_title_comp.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER)
        block_title_comp.set_vertical_alignment(unreal.VerticalTextAligment.EVRTA_TEXT_CENTER)
        block_title_comp.set_world_size(BLOCK_TITLE_SIZE)
        block_color = get_color_by_index(block_idx, block_count)
        block_title_comp.set_text_render_color(block_color)

        # 生成底板
        board_location = unreal.Vector(
            block_origin_x + block_width / 2,
            block_origin_y + block_height / 2,
            SPHERE_HEIGHT - 120
        )
        board_actor:unreal.StaticMeshActor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor,
            board_location
        )
        board_actor.set_actor_label(f"BlockBoard_{folder}")
        board_actor.set_folder_path(folder_path)
        board_actor.static_mesh_component.set_static_mesh(box_mesh)
        board_actor.set_actor_scale3d(unreal.Vector(
            max(cols * 1.1, 1) * SPACING / 100,
            max(rows * 1.1, 1) * SPACING / 100,
            0.2
        ))
        if board_material and isinstance(board_material, unreal.MaterialInterface):
            board_actor.static_mesh_component.set_material(0, board_material)
            
        # 生成球体和文字
        for idx, (mat_path, mat_folder, mat_name) in enumerate(mats):
            row = idx // cols
            col = idx % cols
            x = block_origin_x + col * SPACING
            y = block_origin_y + row * SPACING

            location = unreal.Vector(x, y, SPHERE_HEIGHT)
            sphere_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
                unreal.StaticMeshActor,
                location
            )
            sphere_actor.set_actor_label(f"Sphere_{mat_name}")
            sphere_actor.static_mesh_component.set_static_mesh(sphere_mesh)
            sphere_actor.set_folder_path(folder_path)
            material = unreal.EditorAssetLibrary.load_asset(mat_path)

            if material and isinstance(material, unreal.MaterialInterface):
                sphere_actor.static_mesh_component.set_material(0, material)
            else:
                unreal.log_warning(f"{mat_path} 不是有效的材质，未设置到球体上。")

            text_location = unreal.Vector(x, y, TEXT_HEIGHT)
            text_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
                unreal.TextRenderActor,
                text_location
            )
            text_actor.attach_to_actor(sphere_actor, "", unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD, unreal.AttachmentRule.KEEP_WORLD)
            text_actor.set_actor_label(f"Text_{mat_name}")
            text_actor.set_folder_path(folder_path)
            text_comp = text_actor.text_render
            text_comp.set_text(mat_name)
            text_comp.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER)
            text_comp.set_vertical_alignment(unreal.VerticalTextAligment.EVRTA_TEXT_CENTER)
            text_comp.set_world_size(TEXT_SIZE)

    unreal.log(f"Created spheres by folder with title from {MATERIAL_DIR}")

    
if __name__ == "__main__":
    create_spheres_for_materials()