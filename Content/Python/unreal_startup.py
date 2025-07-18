import unreal
import unreal_uiutils
import unreal_utils
# from unreal_global import *
# from unreal_utils import AssetRegistryPostLoad
unreal.log("""@

####################

Init Start up Script

####################

""")

# assetregistry_pretickhandle = None

# def assetregistry_postload_handle(deltaTime):
#     """
#         Run callback method after registry run to prevent crashed when create new asset at startupS
#     """
#     unreal.log_warning("..Checking Asset Registy Status...")
#     if AssetRegistry.is_loading_assets():
#         unreal.log_warning("..Asset registy still loading...")
#     else:
#         unreal.log_warning("Asset registy ready!")
#         unreal.unregister_slate_post_tick_callback(assetregistry_pretickhandle)
#         AssetRegistryPostLoad.run_callbacks()

# assetregistry_pretickhandle = unreal.register_slate_post_tick_callback(assetregistry_postload_handle)

# import BlueprintLibrary
import UserInterfaces

# startup_bp = unreal.load_asset('/JKTools/EUO_JKStartupObject.EUO_JKStartupObject')
# editor_subsystem = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
# editor_subsystem.try_run(startup_bp)

def reload():
    import importlib

    # importlib.reload(BlueprintLibrary)
    for mod in [unreal_utils, unreal_uiutils, UserInterfaces]:
        importlib.reload(mod)

unreal_uiutils.refresh_toolmenus()
