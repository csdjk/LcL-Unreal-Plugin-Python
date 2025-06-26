import unreal
from Content.Python.test.ue_menu_manager import MenuCommand


class HideActorsCommand(MenuCommand):
    """隐藏选中Actor的命令"""
    
    def __init__(self):
        super().__init__(
            name="HideSelectedActor",
            label="隐藏选中物体",
            tooltip="将选中的Actor在游戏中隐藏"
        )
    
    def execute_command(self):
        actors = unreal.EditorLevelLibrary.get_selected_level_actors()
        for actor in actors:
            actor:unreal.Actor
            actor.set_actor_hidden_in_game(True)
            actor.set_is_temporarily_hidden_in_editor(True)
            unreal.log(f"隐藏了--: {actor.get_name()}")
            
    def _create_command_class(self):
        """为HideActorsCommand创建专属处理类"""
        command_instance = self
        
        @unreal.uclass()
        class HideActorsCommandHandler(unreal.ToolMenuEntryScript):
            def __init__(self):
                super().__init__()
                self.data = unreal.ToolMenuEntryScriptData()
                self.data.name = command_instance.name
                self.data.label = command_instance.label
                self.data.section = command_instance.section
                self.data.tool_tip = command_instance.tooltip
            
            @unreal.ufunction(override=True)
            def execute(self, context):
                command_instance.execute_command()
                
        return HideActorsCommandHandler


class ShowActorsCommand(MenuCommand):
    """显示选中Actor的命令"""
    
    def __init__(self):
        super().__init__(
            name="ShowSelectedActor",
            label="显示选中物体",
            tooltip="将选中的Actor在游戏中显示"
        )
    
    def execute_command(self):
        actors = unreal.EditorLevelLibrary.get_selected_level_actors()
        for actor in actors:
            actor:unreal.Actor
            actor.set_actor_hidden_in_game(False)
            actor.set_is_temporarily_hidden_in_editor(False)  # 同时取消在编辑器中的隐藏
            unreal.log(f"显示了--: {actor.get_name()}")
            
    def _create_command_class(self):
        """为ShowActorsCommand创建专属处理类"""
        command_instance = self
        
        @unreal.uclass()
        class ShowActorsCommandHandler(unreal.ToolMenuEntryScript):
            def __init__(self):
                super().__init__()
                self.data = unreal.ToolMenuEntryScriptData()
                self.data.name = command_instance.name
                self.data.label = command_instance.label
                self.data.section = command_instance.section
                self.data.tool_tip = command_instance.tooltip
            
            @unreal.ufunction(override=True)
            def execute(self, context):
                command_instance.execute_command()
                
        return ShowActorsCommandHandler

