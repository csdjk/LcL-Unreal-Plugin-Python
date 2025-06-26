import unreal 
from unreal import EditorLevelLibrary



def hide_select_actor():
    unreal.log(f"隐藏了--: ")
    
    # actors = EditorLevelLibrary.get_selected_level_actors()
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_selected_level_actors()
    # selected_actors = unreal.EditorUtilityLibrary.get_selected_actors()
    for actor in actors:
        actor:unreal.Actor
        actor.set_actor_hidden_in_game(True)
        actor.set_is_temporarily_hidden_in_editor(True)
        unreal.log(f"隐藏了--: {actor.get_name()}")

def show_select_actor():
    
    actors = EditorLevelLibrary.get_selected_level_actors()
    for actor in actors:
        actor:unreal.Actor
        actor.set_actor_hidden_in_game(False)
        actor.set_is_temporarily_hidden_in_editor(False)  # 同时取消在编辑器中的隐藏
        unreal.log(f"显示了--: {actor.get_name()}")