import unreal
import os
import time
import uuid
import shutil
from pathlib import Path

"""
纹理通道迁移工具 (Texture Channel Transfer Tool)
版本: 1.0

功能说明:
本脚本用于将一组M(Mask)纹理的蓝色通道(B)自动迁移到对应D(Diffuse/Albedo)纹理的Alpha通道(A)中。
主要用于批量处理材质纹理，简化美术工作流程，优化纹理通道的使用。

具体功能:
1. 自动识别同一目录下的配对M和D纹理(基于命名规则: 基础名称+"_m"和"_d")
2. 将M纹理中的B通道提取并替换到D纹理的Alpha通道
3. 保留原始D纹理的所有重要设置(压缩方式、MipMap设置、寻址模式等)
4. 维护所有对D纹理的引用关系(如材质中的引用)，确保修改后引用不丢失

使用方法:
1. 在内容浏览器中选择包含M和D纹理对的目标文件夹
2. 运行此脚本
3. 脚本将自动处理选中文件夹中的所有匹配纹理对

注意事项:
- 需要PIL库支持(如未安装，请在UE的Python环境中运行: pip install pillow)
- 脚本会临时将纹理导出到项目Temp目录中进行处理，完成后会自动清理
- 处理过程不会修改原始M纹理，仅修改D纹理的Alpha通道

"""

def process_textures():
    # 获取当前在内容浏览器中选择的文件夹
    selected_folders = unreal.EditorUtilityLibrary.get_selected_folder_paths()
    
    if not selected_folders or len(selected_folders) == 0:
        unreal.log_warning("请先在内容浏览器中选择一个文件夹，然后再运行此脚本")
        return
    
    selected_path = selected_folders[0]
    selected_path = selected_path.replace("/All", "")
    unreal.log_warning(f"处理目录: {selected_path}")
    
    # 获取所有Texture2D资产
    assets = unreal.PythonBPLib.get_assets_data_by_class(
        paths_folders=[selected_path], 
        class_names=["Texture2D"],
    )
    
    unreal.log_warning(f"在目录 {selected_path} 中找到 {len(assets)} 个纹理资产")
    
    # 将获取的资产整理到字典中
    texture_assets = {}
    for asset in assets:
        asset_name = str(asset.asset_name)
        package_path = str(asset.package_path)
        package_name = str(asset.package_name)
        texture_assets[asset_name] = (package_path, package_name)
        # unreal.log(f"资产: {asset_name}, 路径: {package_name}")
    
    # 建立_m和_d纹理的映射关系
    m_textures = {}
    d_textures = {}
        
    for texture_name, (package_path, package_name) in texture_assets.items():
        if "_m" in texture_name:
            base_name = texture_name.split("_m")[0]
            m_textures[base_name] = (texture_name, package_path, package_name)
        elif "_d" in texture_name:
            base_name = texture_name.split("_d")[0]
            d_textures[base_name] = (texture_name, package_path, package_name)
    
    unreal.log_warning(f"找到 {len(m_textures)} 个_m纹理和 {len(d_textures)} 个_d纹理")
    
    # 创建临时目录 - 使用UE项目临时目录而不是系统临时目录
    project_dir = unreal.Paths.project_dir()
    temp_base_dir = os.path.join(project_dir, "Temp")
    temp_dir = os.path.join(temp_base_dir, f"TextureProcess_{uuid.uuid4().hex}")
    
    # 确保目录存在
    try:
        os.makedirs(temp_dir, exist_ok=True)
        unreal.log(f"创建临时目录: {temp_dir}")
    except Exception as e:
        unreal.log_error(f"无法创建临时目录: {e}")
        return
    
    # 检查并处理纹理对
    processed_count = 0
    
    # 准备批量导出
    texture_pairs = []
    
    for base_name in m_textures:
        if base_name in d_textures:
            m_texture_name, m_package_path, m_package_name = m_textures[base_name]
            d_texture_name, d_package_path, d_package_name = d_textures[base_name]
            
            # unreal.log(f"准备处理纹理对: {base_name}")
            # unreal.log(f"M纹理: {m_texture_name}, 路径: {m_package_name}")
            # unreal.log(f"D纹理: {d_texture_name}, 路径: {d_package_name}")
            
            # 记录纹理对，便于后续处理
            texture_pairs.append((
                base_name,
                m_texture_name, m_package_path, m_package_name,
                d_texture_name, d_package_path, d_package_name
            ))
    
    try:
        # 获取AssetTools实例
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        
        # 创建两个导出目录
        m_export_dir = os.path.join(temp_dir, "m_textures")
        d_export_dir = os.path.join(temp_dir, "d_textures")
        
        os.makedirs(m_export_dir, exist_ok=True)
        os.makedirs(d_export_dir, exist_ok=True)
        
        # 处理每一对纹理
        for (base_name, m_texture_name, m_package_path, m_package_name, 
             d_texture_name, d_package_path, d_package_name) in texture_pairs:
            
            try:
                unreal.log(f"处理纹理对: {base_name}")
                
                # 获取原始D纹理资产以保存其设置
                d_asset = unreal.EditorAssetLibrary.load_asset(d_package_name)
                if not d_asset:
                    unreal.log_error(f"无法加载D纹理资产: {d_package_name}")
                    continue
                
                # 保存原始D纹理的所有重要设置
                d_texture_settings = {
                    # 基本设置组
                    "compression_settings": d_asset.get_editor_property("compression_settings"),
                    "srgb": d_asset.get_editor_property("srgb"),
                    "filter": d_asset.get_editor_property("filter"),
                    "mip_gen_settings": d_asset.get_editor_property("mip_gen_settings"),
                    
                    # 纹理寻址设置
                    "address_x": d_asset.get_editor_property("address_x") if hasattr(d_asset, "address_x") else None,
                    "address_y": d_asset.get_editor_property("address_y") if hasattr(d_asset, "address_y") else None,
                    
                    # LOD和流送设置
                    "lod_bias": d_asset.get_editor_property("lod_bias") if hasattr(d_asset, "lod_bias") else None,
                    "lod_group": d_asset.get_editor_property("lod_group") if hasattr(d_asset, "lod_group") else None,
                    "never_stream": d_asset.get_editor_property("never_stream") if hasattr(d_asset, "never_stream") else None,
                    
                    # 压缩和质量设置
                    "compression_quality": d_asset.get_editor_property("compression_quality") if hasattr(d_asset, "compression_quality") else None,
                    "compression_no_alpha": d_asset.get_editor_property("compression_no_alpha") if hasattr(d_asset, "compression_no_alpha") else None,
                    "defer_compression": d_asset.get_editor_property("defer_compression") if hasattr(d_asset, "defer_compression") else None,
                    "lossy_compression_amount": d_asset.get_editor_property("lossy_compression_amount") if hasattr(d_asset, "lossy_compression_amount") else None,
                    
                    # Mip和缩放设置
                    "power_of_two_mode": d_asset.get_editor_property("power_of_two_mode") if hasattr(d_asset, "power_of_two_mode") else None,
                    "max_texture_size": d_asset.get_editor_property("max_texture_size") if hasattr(d_asset, "max_texture_size") else None,
                    "downscale": d_asset.get_editor_property("downscale") if hasattr(d_asset, "downscale") else None,
                    
                    # 颜色和通道设置
                    "flip_green_channel": d_asset.get_editor_property("flip_green_channel") if hasattr(d_asset, "flip_green_channel") else None,
                    "use_legacy_gamma": d_asset.get_editor_property("use_legacy_gamma") if hasattr(d_asset, "use_legacy_gamma") else None,
                    "chroma_key_texture": d_asset.get_editor_property("chroma_key_texture") if hasattr(d_asset, "chroma_key_texture") else None,
                    
                    # 虚拟纹理设置
                    "virtual_texture_streaming": d_asset.get_editor_property("virtual_texture_streaming") if hasattr(d_asset, "virtual_texture_streaming") else None,
                }
                
                # 提取包路径的最后部分作为资产名称
                m_asset_filename = os.path.basename(m_package_name)
                d_asset_filename = os.path.basename(d_package_name)
                
                # 导出M纹理和D纹理
                asset_tools.export_assets([m_package_name], m_export_dir)
                asset_tools.export_assets([d_package_name], d_export_dir)
                
                # 等待文件确实被写入磁盘
                time.sleep(0.5)
                
                # 寻找M纹理和D纹理的导出文件
                m_export_path = None
                d_export_path = None
                
                # 递归寻找导出的文件
                for root, dirs, files in os.walk(m_export_dir):
                    for file in files:
                        if m_asset_filename in file:
                            m_export_path = os.path.join(root, file)
                            break
                    if m_export_path:
                        break
                
                for root, dirs, files in os.walk(d_export_dir):
                    for file in files:
                        if d_asset_filename in file:
                            d_export_path = os.path.join(root, file)
                            break
                    if d_export_path:
                        break
                
                if m_export_path is None or d_export_path is None:
                    unreal.log_error(f"无法找到导出的纹理文件: M={m_export_path}, D={d_export_path}")
                    continue
                
                # unreal.log(f"找到M纹理文件: {m_export_path}")
                # unreal.log(f"找到D纹理文件: {d_export_path}")
                
                # 调用Python图像处理库来修改纹理
                try:
                    
                    from PIL import Image
    
                    # 打开两个图像(增加重试机制)
                    retry_count = 0
                    m_img = None
                    d_img = None
                    
                    while retry_count < 5:
                        try:
                            m_img = Image.open(m_export_path)
                            d_img = Image.open(d_export_path)
                            break
                        except Exception as e:
                            retry_count += 1
                            unreal.log_warning(f"尝试打开图像时遇到错误，重试 {retry_count}/5: {str(e)}")
                            time.sleep(1)
                    
                    if m_img is None or d_img is None:
                        unreal.log_error("无法打开导出的图像文件")
                        continue
                    
                    # 检查图像模式并转换为RGBA
                    m_img = m_img.convert("RGBA")
                    d_img = d_img.convert("RGBA")
                    
                    # 记录尺寸，用于调试
                    m_size = m_img.size
                    d_size = d_img.size
                    
                    # 检查尺寸是否匹配，如果不匹配则调整M纹理大小
                    if m_size != d_size:
                        # unreal.log_warning(f"纹理尺寸不匹配! M: {m_size}, D: {d_size}，正在调整M纹理尺寸...")
                        m_img = m_img.resize(d_size, Image.Resampling.LANCZOS)
                    
                    # 拆分通道
                    m_r, m_g, m_b, m_a = m_img.split()
                    d_r, d_g, d_b, d_a = d_img.split()
                    
                    # 再次检查通道尺寸是否匹配
                    if m_b.size != d_r.size:
                        # unreal.log_warning(f"通道尺寸仍不匹配! M蓝通道: {m_b.size}, D红通道: {d_r.size}，正在调整通道尺寸...")
                        m_b = m_b.resize(d_r.size, Image.Resampling.LANCZOS)
                    
                    # 检查B通道是否所有像素都是白色
                    import numpy as np
                    m_b_array = np.array(m_b)
                    if np.all(m_b_array == 255):
                        unreal.log_warning(f"---跳过复制通道：{base_name} 的B通道所有像素都是255（白色）")
                        continue
                    
                    unreal.log_warning(f"===正在处理纹理对: {base_name} (M: {m_texture_name}, D: {d_texture_name})")
                    
                    # 将M纹理的B通道用作D纹理的A通道
                    new_dimg = Image.merge("RGBA", (d_r, d_g, d_b, m_b))
                    
                    # 直接覆盖原始D纹理文件
                    # 先保存到一个临时文件
                    temp_output_path = os.path.splitext(d_export_path)[0] + "_temp.tga"
                    new_dimg.save(temp_output_path, format="TGA")
                    
                    # 确认文件已经写入磁盘
                    retry_count = 0
                    while not os.path.exists(temp_output_path) and retry_count < 5:
                        time.sleep(0.5)
                        retry_count += 1
                    
                    if not os.path.exists(temp_output_path):
                        unreal.log_error(f"无法保存修改后的纹理: {temp_output_path}")
                        continue
                    
                    # 删除原始D纹理文件，然后将临时文件重命名为原始文件名
                    try:
                        if os.path.exists(d_export_path):
                            os.remove(d_export_path)
                        os.rename(temp_output_path, d_export_path)
                        # unreal.log_warning(f"成功覆盖原始D纹理文件: {d_export_path}")
                    except Exception as e:
                        unreal.log_error(f"覆盖原始文件时出错: {str(e)}")
                        continue

                

                    # 导入纹理
                    imported_asset = unreal.AssetImportTask()
                    imported_asset.filename = d_export_path
                    imported_asset.destination_path = d_package_path
                    imported_asset.destination_name = d_asset_filename
                    imported_asset.replace_existing = True
                    imported_asset.save = True
                    imported_asset.automated = True
                    
                    asset_tools.import_asset_tasks([imported_asset])
                    
                    # 获取新导入的资产
                    new_dasset = unreal.EditorAssetLibrary.load_asset(d_package_name)
                    if not new_dasset:
                        unreal.log_error(f"导入后无法加载D纹理资产: {d_package_name}")
                        continue
                    
                    # 应用原始设置到新纹理
                    # unreal.log(f"应用原始纹理设置到新导入的纹理")
                    
                    # 应用所有保存的设置到新纹理
                    for prop_name, prop_value in d_texture_settings.items():
                        if prop_value is not None:
                            try:
                                new_dasset.set_editor_property(prop_name, prop_value)
                            except Exception as e:
                                unreal.log_warning(f"无法设置属性 {prop_name}: {str(e)}")
                    
                    # 保存资产
                    unreal.EditorAssetLibrary.save_loaded_asset(new_dasset)
                    
                    unreal.log(f"成功将修改后的纹理导入回引擎，覆盖了: {d_package_name}")
                    unreal.log(f"保留了原始纹理的所有重要设置")
                    processed_count += 1
                
                except ImportError as ie:
                    unreal.log_error(f"缺少PIL库: {str(ie)}")
                    unreal.log_error("请先在UE的Python环境中安装PIL: pip install pillow")
                
                except Exception as e:
                    unreal.log_error(f"处理图像时发生错误: {str(e)}")
                    import traceback
                    unreal.log_error(traceback.format_exc())
            
            except Exception as e:
                unreal.log_error(f"处理贴图 {base_name} 时发生错误: {str(e)}")
                import traceback
                unreal.log_error(traceback.format_exc())
    
    except Exception as e:
        unreal.log_error(f"导出资产时发生错误: {str(e)}")
        import traceback
        unreal.log_error(traceback.format_exc())
    
    # 清理临时文件
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
        unreal.log(f"已尝试清理临时目录: {temp_dir}")
    except Exception as e:
        unreal.log_warning(f"清理临时文件时发生错误: {e}")
    
    unreal.log(f"处理完成! 共处理了 {processed_count} 对纹理。")

# 直接执行函数
process_textures()