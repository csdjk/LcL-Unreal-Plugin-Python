import unreal
import unreal_uiutils
import unreal_startup


# me_reloadbutton = unreal_uiutils.create_python_tool_menu_entry(
#     name="ReloadScriptsBtn",
#     label="Reload Script",
#     command_string="import importlib; import unreal_startup; importlib.reload(unreal_startup); unreal_startup.reload()",
# )
# tb_reloadbutton = unreal_uiutils.create_toolbar_button(
#     name="ReloadBtn",
#     label="PyReload",
#     command_string="print('Reloaded!')",
# )
# me_quitbutton = unreal_uiutils.create_python_tool_menu_entry(
#     name="RestartUnrealBtn",
#     label="Restart Unreal",
#     command_string="import unreal_utils; unreal_utils.restart_editor()",
# )

# new_mainmenu = unreal_uiutils.extend_mainmenu("LcLTools", "LcL Tools")
# utils_section = new_mainmenu.add_section("utilities", "Utilities Tools")
# new_mainmenu.add_menu_entry("utilities", me_reloadbutton)
# new_mainmenu.add_menu_entry("utilities", me_quitbutton)
# asset_tools = new_mainmenu.add_section("assettools", "Asset Tools")
# new_mainmenu.add_menu_entry("assettools", me_renameassetbutton)
# print('Reloaded!')
