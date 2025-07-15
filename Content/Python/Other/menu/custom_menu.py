import unreal

# 获取所有菜单对象的入口点
menus = unreal.ToolMenus.get()

# 创建主编辑器菜单的自定义菜单
# 查找主级编辑器的主菜单
main_menu = menus.find_menu("LevelEditor.MainMenu")
# 在主菜单中添加名为"Custom Menu"的子菜单，内部标识为"LcL-Tools"
test_menu = main_menu.add_sub_menu("Custom Menu", "Python Automation", "LcL-Tools", "LcL-Tools")

# 刷新所有菜单组件以应用更改
menus.refresh_all_widgets()


@unreal.uclass()
class Test(unreal.ToolMenuEntryScript):
    """示例类，用于注册和处理主编辑器菜单项的点击事件"""
    @unreal.ufunction(override=True)
    def execute(self, context):
        # 当菜单项被点击时执行此函数
        unreal.log("LcL-Tools 菜单项被点击了！")
        
# 创建主编辑器菜单项
script_object = Test()
# 初始化菜单项配置
script_object.init_entry(
    owner_name=test_menu.menu_name,  # 菜单项的所有者名称
    menu=test_menu.menu_name,        # 菜单项所属的菜单名称
    section="CustomSection",         # 菜单项的分区名称（下划线）
    name="TestMenuItem",             # 菜单项的内部名称
    label="TestMenuItem",            # 菜单项显示的标签
    tool_tip="这是一个测试菜单项",    # 鼠标悬停时显示的提示信息
)
# 注册菜单项到菜单系统
script_object.register_menu_entry()


@unreal.uclass()
class Test2(unreal.ToolMenuEntryScript):
    """示例类，用于注册和处理主编辑器菜单项的点击事件"""
    @unreal.ufunction(override=True)
    def execute(self, context):
        # 当菜单项被点击时执行此函数
        unreal.log("LcL-Tools 菜单项被点击了2！")
        
        
# 创建StaticMesh编辑器菜单的自定义菜单
# 查找StaticMesh编辑器的主菜单
staticmesh_menu = menus.find_menu("ContentBrowser.AssetContextMenu.StaticMesh")

# test_menu2 = main_menu.add_sub_menu("Custom Menu", "Python Automation", "LcL-Tools", "LcL-Tools")

# script_object2 = Test2()

# script_object2.init_entry(
#     owner_name=test_menu2.menu_name,  # 菜单项的所有者名称
#     menu=test_menu2.menu_name,        # 菜单项所属的菜单名称
#     section="CustomSection",         # 菜单项的分区名称（下划线）
#     name="TestMenuItem2",             # 菜单项的内部名称
#     label="TestMenuItem2",            # 菜单项显示的标签
#     tool_tip="这是一个测试菜单项",    # 鼠标悬停时显示的提示信息
# )
# 初始化StaticMesh编辑器菜单项配置
# script_object2.init_entry(
#     owner_name=staticmesh_menu.menu_name,  # 菜单项的所有者名称
#     menu=staticmesh_menu.menu_name,        # 菜单项所属的菜单名称
#     section="GetAssetActions",               # 菜单项的分区名称（下划线）
#     name="CustomStaticMeshTestMenuItem",         # 菜单项的内部名称
#     label="CustomStaticMeshTestMenuItem",        # 菜单项显示的标签
#     tool_tip="这是一个StaticMesh测试菜单项",  # 鼠标悬停时显示的提示信息
# )
# script_object2.register_menu_entry()

print(staticmesh_menu)





# 获取 LevelEditor 工具栏菜单
# toolbar_menu = menus.find_menu("LevelEditor.LevelEditorToolBar")

# @unreal.uclass()
# class ToolbarButton(unreal.ToolMenuEntryScript):
#     @unreal.ufunction(override=True)
#     def execute(self, context):
#         unreal.log("自定义工具栏按钮被点击！")

# toolbar_button = ToolbarButton()
# toolbar_button.init_entry(
#     owner_name=toolbar_menu.menu_name,
#     menu=toolbar_menu.menu_name,
#     section="Settings",  # 工具栏常用的分区有"Settings"、"Compile"等
#     name="LcLToolbarButton",
#     label="LcL按钮",
#     tool_tip="这是一个自定义工具栏按钮"
# )
# toolbar_button.register_menu_entry()

# menus.refresh_all_widgets()
