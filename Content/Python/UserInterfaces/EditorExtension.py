import unreal_uiutils
import unreal_utils
import unreal

def extend_editor_example():
    # declare menu entry
    me_reloadbutton = unreal_uiutils.create_python_tool_menu_entry(
        name="ReloadScriptsBtn",
        label="Reload Script",
        command_string="import importlib; import unreal_startup; importlib.reload(unreal_startup); unreal_startup.reload()",
    )
    me_quitbutton = unreal_uiutils.create_python_tool_menu_entry(
        name="RestartUnrealBtn",
        label="Restart Unreal",
        command_string="import unreal_utils; unreal_utils.restart_editor()",
    )
    me_renameassetbutton = unreal_uiutils.create_python_tool_menu_entry(
        name="RenameAssetBtn",
        label="Rename Assets",
        command_string="unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem).spawn_and_register_tab(unreal.load_asset('/JKTools/UI/Tools/EUW_JK_RenameTool.EUW_JK_RenameTool'))",
    )
    # This create a button on toolboard
    tb_reloadbutton = unreal_uiutils.create_toolbar_button(
        name="ReloadBtn",
        label="PyReload",
        command_string="import importlib; import unreal_startup; importlib.reload(unreal_startup); unreal_startup.reload()",
    )

    # This create a drop down button on toolboard
    # tb_combobutton = unreal_uiutils.create_toolbar_combo_button(
    #     "comboBtn", "python.tools"
    # )
    #TODO: Find out where it is possible to register a new context menu for combo button

    # create submenu in 'File' Menu and register menu entry created above
    # pythonsubmenu = unreal_uiutils.extend_mainmenu_item(
    #     "File", "PythonTools", "PythonTools", "Python Tools"
    # )
    # pythonsubmenu.add_section("python.file.menu", "Python Tools")
    # pythonsubmenu.add_menu_entry("python.file.menu", me_reloadbutton)
    # pythonsubmenu.add_menu_entry("python.file.menu", me_quitbutton)

    # Create Standalone Menu and register menu entry created above
    new_mainmenu = unreal_uiutils.extend_mainmenu("JKTools", "JKTools")
    utils_section = new_mainmenu.add_section("utilities", "Utilities Tools")
    new_mainmenu.add_menu_entry("utilities", me_reloadbutton)
    new_mainmenu.add_menu_entry("utilities", me_quitbutton)
    asset_tools = new_mainmenu.add_section("assettools", "Asset Tools")
    new_mainmenu.add_menu_entry("assettools", me_renameassetbutton)

    # Extend Asset Context Menu
    sub_asset_context_menu = unreal_uiutils.extend_toolmenu(unreal_uiutils.get_asset_context_menu(), "JKAssetContextMenu", "JK Asset Actions")
    sub_asset_context_menu.add_section("jk.assetmenu", "Tools")
    sub_asset_context_menu.add_menu_entry("python.assetmenu", me_renameassetbutton)


    # Extend Actor Context Menu
    # actor_context_menu = unreal_uiutils.get_actor_context_menu()
    # actor_context_menu.add_section("jk.actoractions", "Tools")
    # sub_actor_context_menu = actor_context_menu.add_sub_menu(actor_context_menu.menu_name, "jk.actoractions", "JKActorContextMenu", "JK Actor Actions")
    # sub_actor_context_menu.add_section("jk.actormenu", "Tools")
    # action_sampleactorprint = unreal_uiutils.create_python_tool_menu_entry(
    #     name="SampleActorTool",
    #     label="Print Selected Actor",
    #     command_string='print(LevelLibrary.get_selected_level_actors())',
    # )
    # sub_actor_context_menu.add_menu_entry("jk.actormenu", action_sampleactorprint)
    # actor_context_menu.add_menu_entry("python.actoractions", action_sampleactorprint)

# AssetRegistryPostLoad.register_callback(extend_editor)

def extend_editor():
    # declare menu entry
    me_reloadbutton = unreal_uiutils.create_python_tool_menu_entry(
        name="ReloadScriptsBtn",
        label="重载脚本",
        command_string="import importlib; import unreal_startup; importlib.reload(unreal_startup); unreal_startup.reload()",
    )
    #创建独立菜单并注册上面创建的菜单项
    new_mainmenu = unreal_uiutils.extend_mainmenu("LcLTools", "LcL Tools")
    utils_section = new_mainmenu.add_section("reload", "Reload Tools")
    new_mainmenu.add_menu_entry("reload", me_reloadbutton)
    
    # =========================================工具栏 按钮======================================================
     # This create a button on toolboard
    unreal_uiutils.create_toolbar_button(
        name="RestartUnrealBtn",
        label="RestartUE",
        tool_tip="重启UE编辑器",
        icons = ["EditorStyle", "Cascade.RestartInLevel.Small"],
        command_string="import unreal_utils; unreal_utils.restart_editor()",
    )
   
    unreal_uiutils.create_toolbar_button(
        name="ShowActor",
        label="Show",
        tool_tip="显示选中的Actor",
        icons = ["EditorStyle", "GenericViewButton"],
        command_string="from UserInterfaces import quick_hide; quick_hide.show_select_actor()",
    )
    unreal_uiutils.create_toolbar_button(
        name="HideActor",
        label="Hide",
        tool_tip="隐藏选中的Actor",
        icons = ["EditorStyle", "Kismet.VariableList.HideForInstance"],
        command_string="from UserInterfaces import quick_hide; quick_hide.hide_select_actor()",
    )
    
    # 菜单
    # me_test = unreal_uiutils.create_python_tool_menu_entry(
    #     name="TestBtn",
    #     label="Test",
    #     command_string="from UserInterfaces import quick_hide; quick_hide.hide_select_actor()",
    # )
    # new_mainmenu.add_menu_entry("utilities", me_test)

extend_editor()
