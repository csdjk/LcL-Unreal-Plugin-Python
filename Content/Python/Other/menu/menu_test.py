# code in init_unreal.py wil run on startup if the plugin is enabled
import unreal


section_name = "Plugins"
se_command = 'print("Test")'
label = "LcL-Tools2"
tooltip = "my tooltip"


@unreal.uclass()
class Test(unreal.ToolMenuEntryScript):

    def __init__(self):
        super().__init__()
        self.data: unreal.ToolMenuEntryScriptData
        self.data.name = "TestEntry"
        self.data.label = "TestEntryLabel"
        self.data.section = "TestSection"
        self.data.tool_tip = "This is a test entry"

    @unreal.ufunction(override=True)
    def execute(self, context):
        # 当菜单项被点击时执行此函数
        unreal.log("LcL-Tools 菜单项被点击了！")


def create_script_editor_button():
    """Add a tool button to the tool bar"""
    section_name = "Plugins"
    label = "LcL-Tools"
    tooltip = "my tooltip"

    menus = unreal.ToolMenus.get()
    level_menu_bar = menus.find_menu("LevelEditor.LevelEditorToolBar.PlayToolBar")
    level_menu_bar.add_section(section_name=section_name, label=section_name)

    entry = unreal.ToolMenuEntry(type=unreal.MultiBlockType.TOOL_BAR_BUTTON)
    entry.set_label(label)
    entry.set_tool_tip(tooltip)
    entry.set_icon("EditorStyle", "DebugConsole.Icon")
    level_menu_bar.add_menu_entry(section_name, entry)
    menus.refresh_all_widgets()


def main():
    menus = unreal.ToolMenus.get()
    main_menu = menus.find_menu("LevelEditor.MainMenu")

    # 创建脚本对象
    script_obj = Test()

    # 创建菜单项并设置脚本对象
    entry = unreal.ToolMenuEntry(
        type=unreal.MultiBlockType.MENU_ENTRY,
        script_object=script_obj,
    )

    script_menu = main_menu.add_sub_menu(
        main_menu.get_name(), "SectionTest2", "NameTest2", "Test2"
    )
    script_menu.add_menu_entry("Scripts", entry)
    menus.refresh_all_widgets()


main()
