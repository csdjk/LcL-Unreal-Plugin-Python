# code in init_unreal.py wil run on startup if the plugin is enabled
import unreal

# @unreal.uclass()
# class Test(unreal.ToolMenuEntryScript):

#     def __init__(self):
#         super().__init__()
#         self.data: unreal.ToolMenuEntryScriptData
#         self.data.name = "TestEntry"
#         self.data.label = "TestEntryLabel"
#         self.data.section = "TestSection"
#         self.data.tool_tip = "This is a test entry"

#     @unreal.ufunction(override=True)
#     def execute(self, context):
#         # 当菜单项被点击时执行此函数
#         unreal.log("LcL-Tools 菜单项被点击了！")

# selected_actors = unreal.EditorUtilityLibrary().get_selected_level_actors()
# print(f"Selected folders: {selected_actors}")
editor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
selected_actors = editor_subsystem.get_selected_level_actors()
print(f"Selected folders: {selected_actors}")


test = unreal.PythonBPLib.get_selected_components()
print(f"Selected test: {test}")
