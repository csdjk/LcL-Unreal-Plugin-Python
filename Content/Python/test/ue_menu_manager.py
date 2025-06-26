import unreal

class UE5MenuManager:
    """虚幻引擎菜单管理器，用于创建和管理自定义菜单项"""
    
    # 常用菜单类型枚举
    class MenuType:
        # 主要菜单
        MAIN_MENU = "LevelEditor.MainMenu"
        # 工具栏
        PLAY_TOOLBAR = "LevelEditor.LevelEditorToolBar.PlayToolBar"
        LEVEL_TOOLBAR = "LevelEditor.LevelEditorToolBar"
        USER_TOOLBAR = "LevelEditor.LevelEditorToolBar.User"
        # 上下文菜单
        ACTOR_CONTEXT_MENU = "LevelEditor.ActorContextMenu"
        CONTENT_BROWSER_ASSET_CONTEXT_MENU = "ContentBrowser.AssetContextMenu"
        # 特定资产上下文菜单
        MATERIAL_CONTEXT_MENU = "ContentBrowser.AssetContextMenu.MaterialInterface"
        BLUEPRINT_CONTEXT_MENU = "ContentBrowser.AssetContextMenu.Blueprint"
        STATIC_MESH_CONTEXT_MENU = "ContentBrowser.AssetContextMenu.StaticMesh"
        SKELETAL_MESH_CONTEXT_MENU = "ContentBrowser.AssetContextMenu.SkeletalMesh"
        TEXTURE_CONTEXT_MENU = "ContentBrowser.AssetContextMenu.Texture"
        # 其他
        SCENE_OUTLINER_CONTEXT_MENU = "LevelEditor.LevelEditorSceneOutliner.ContextMenu"
        CONTENT_BROWSER_ADD_NEW = "ContentBrowser.AddNewContextMenu"
    
    def __init__(self, section="Python Automation", menu_name="LcL-Tools"):
        """
        初始化菜单管理器
        Args:
            menu_name: 显示在UI上的菜单名称
            section: 菜单的内部标识符
        """
        self.section = section
        self.menu_name = menu_name
        self.menus = unreal.ToolMenus.get()
        self.commands = []
        
    def add_main_menu(self, command, menu_type=None, section_name=None, sub_menu_name=None):
        """
        注册命令到指定菜单
        
        Args:
            command: 要注册的命令
            menu_type: 菜单类型，使用MenuType中的常量，默认为MAIN_MENU
            section_name: 菜单区域名称，默认使用command.section
            sub_menu_name: 子菜单名称，默认为self.menu_name
        """
        # 设置默认值
        if menu_type is None:
            menu_type = self.MenuType.MAIN_MENU
        
        if section_name is None:
            section_name = command.section
        
        if sub_menu_name is None:
            sub_menu_name = self.menu_name
        
        # 获取目标菜单
        target_menu = self.menus.find_menu(menu_type)
        if not target_menu:
            unreal.log_warning(f"找不到菜单: {menu_type}")
            return
        
        # 添加命令到列表
        self.commands.append(command)
        
        # 根据菜单类型处理
        if menu_type == self.MenuType.MAIN_MENU:
            # 主菜单需要创建子菜单
            custom_menu = target_menu.add_sub_menu(
                "Custom Menu",
                self.section,
                sub_menu_name,
                sub_menu_name
            )
            
            # 确保区域存在
            custom_menu.add_section(section_name=section_name, label=section_name)
            
            # 创建菜单项
            entry = unreal.ToolMenuEntry(
                type=unreal.MultiBlockType.MENU_ENTRY,
                script_object=command.get_script_object(),
            )
            
            # 添加菜单项到自定义菜单
            custom_menu.add_menu_entry(section_name, entry)
        else:
            # 其他菜单直接添加到目标菜单
            # 确保区域存在
            target_menu.add_section(section_name=section_name, label=section_name)
            
            # 创建菜单项
            entry = unreal.ToolMenuEntry(
                type=unreal.MultiBlockType.MENU_ENTRY,
                script_object=command.get_script_object(),
            )
            
            # 添加菜单项
            target_menu.add_menu_entry(section_name, entry)
    
    def add_toolbar_button(self, toolbar_type, label, tooltip, icon_name="EditorStyle.DebugConsole.Icon", command=None, section_name="Plugins"):
        """
        添加按钮到工具栏
        
        Args:
            toolbar_type: 工具栏类型，使用MenuType中的常量
            label: 按钮标签
            tooltip: 按钮提示
            icon_name: 图标名称，格式为"StyleSet.IconName"
            command: 执行的命令对象
            section_name: 区域名称
        """
        # 获取工具栏
        toolbar = self.menus.find_menu(toolbar_type)
        if not toolbar:
            unreal.log_warning(f"找不到工具栏: {toolbar_type}")
            return
        
        # 确保区域存在 - 直接添加区域，不需要检查
        toolbar.add_section(section_name=section_name, label=section_name)
        
        # 解析图标样式和名称
        style_set, icon = "EditorStyle", icon_name
        if "." in icon_name:
            style_set, icon = icon_name.split(".", 1)
        
        # 创建工具栏按钮
        entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
        entry.set_label(label)
        entry.set_tool_tip(tooltip)
        entry.set_icon(style_set, icon)
        
        # 如果提供了命令对象，则设置脚本对象
        if command:
            entry.script_object = command.get_script_object()
        
        # 添加按钮到工具栏
        toolbar.add_menu_entry(section_name, entry)
    
    def create_play_toolbar_button(self, label, tooltip, icon_name="DebugConsole.Icon", command=None):
        """
        添加按钮到PlayToolBar (向后兼容方法)
        
        Args:
            label: 按钮标签
            tooltip: 按钮提示
            icon_name: 图标名称
            command: 执行的命令对象
        """
        self.add_toolbar_button(
            self.MenuType.PLAY_TOOLBAR,
            label,
            tooltip,
            icon_name,
            command
        )
    
    def add_asset_context_menu_item(self, command, asset_type=None, section_name=None):
        """
        添加项目到内容浏览器资产上下文菜单
        
        Args:
            command: 要注册的命令
            asset_type: 特定资产类型的菜单，None表示所有资产
            section_name: 菜单区域名称，默认使用command.section
        """
        menu_type = self.MenuType.CONTENT_BROWSER_ASSET_CONTEXT_MENU
        
        # 如果指定了资产类型，使用对应的上下文菜单
        if asset_type:
            menu_type = f"{menu_type}.{asset_type}"
        
        self.add_main_menu(
            command,
            menu_type=menu_type,
            section_name=section_name
        )
    
    def add_actor_context_menu_item(self, command, section_name=None):
        """
        添加项目到关卡编辑器Actor上下文菜单
        
        Args:
            command: 要注册的命令
            section_name: 菜单区域名称，默认使用command.section
        """
        self.add_main_menu(
            command,
            menu_type=self.MenuType.ACTOR_CONTEXT_MENU,
            section_name=section_name
        )
    
    def refresh_menus(self):
        """刷新所有菜单"""
        self.menus.refresh_all_widgets()


class MenuCommand:
    """菜单命令基类"""
    
    def __init__(self, name, label, tooltip, section="CustomSection"):
        """
        初始化命令
        
        Args:
            name: 命令内部名称
            label: 显示在菜单上的标签
            tooltip: 鼠标悬停时显示的提示文本
            section: 菜单分区名称
        """
        self.name = name
        self.label = label
        self.tooltip = tooltip
        self.section = section
        self._script_object = None
    
    def execute_command(self):
        """执行命令的逻辑，子类需要重写此方法"""
        raise NotImplementedError("子类必须实现execute_command方法")
    
    def get_script_object(self):
        """获取脚本对象，如果不存在则创建"""
        if self._script_object is None:
            self._script_object = self._create_command_class()()
        return self._script_object
    
    def _create_command_class(self):
        """
        创建处理菜单点击事件的类 - 子类必须实现此方法
        返回一个unreal.ToolMenuEntryScript子类
        """
        raise NotImplementedError("子类必须实现_create_command_class方法")
