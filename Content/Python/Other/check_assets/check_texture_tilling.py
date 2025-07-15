import unreal
from unreal import (
    Texture2D,
    TextureAddress

)

texture: Texture2D
print_log: bool

# output
result: bool
log_str: str

def check_texture_tiling(texture: Texture2D, address_x: TextureAddress, address_y: TextureAddress) -> bool:
    """
    检查单个Texture2D的平铺模式
    :param texture: Texture2D资源
    :param address_x: 目标AddressX
    :param address_y: 目标AddressY
    :return: 是否为目标平铺模式
    """
    if not texture:
        unreal.log_warning("传入的Texture2D无效")
        return False
    is_match = (texture.address_x == address_x) and (texture.address_y == address_y)
    
    # log_str = f"{texture.get_path_name()} AddressX={texture.address_x} AddressY={texture.address_y}，目标: X={address_x} Y={address_y}，检测结果: {is_match}"
    log_str = f"""Texture 平铺模式不合规，必须使用{address_x}平铺模式,已自动修复：
                  Texture: {texture.get_path_name()} 
                  AddressX: {texture.address_x} 
                  AddressY: {texture.address_y} 
                  """
    if not is_match:
        texture.address_x = address_x
        texture.address_y = address_y
        unreal.EditorAssetLibrary.save_asset(texture.get_path_name())
    
    return is_match,log_str

result,log_str= check_texture_tiling(texture, TextureAddress.TA_WRAP, TextureAddress.TA_WRAP)