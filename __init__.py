# Copyright PORTALSURFER, No rights reserved.
# https: //www.blender.org/about/license/

import bpy
import importlib
from . import operators
from . import properties
from .functions import graphics, export, utilities
from .ui import header_menu, export_preferences

bl_info = {
    "name": "CFBX",
    "author": "PORTALSURFER",
    "blender": (2, 80, 0),
    "version": (0, 0, 2),
    "location": "Outliner -> ContextMenu -> CFBX",
    "description": "Export active collection as FBX",
    "warning": "",
    "category": "Export"
}

modules = [
    operators,
    properties,
    export_preferences
]

classes = [
    operators.CFBX_OT_export_active_collection,
    operators.CFBX_OT_open_properties,
    operators.CFBX_OT_select_path,
    export_preferences.ExportPreferences,
    header_menu.TOPBAR_MT_CFBX_export,
    header_menu.TOPBAR_MT_CFBX_set_properties
]


def register():
    """
    This function registers the addon classes when the addon is enabled.
    """
    # reload the submodules
    for module in modules:
        importlib.reload(module)

    # register the properties
    properties.register()

    # register the classes
    for cls in classes:
        bpy.utils.register_class(cls)

    header_menu.add_menus()


def unregister():
    """
    This function unregisters the addon classes when the addon is disabled.
    """
    # remove the header menu
    header_menu.remove_menus()

    # unregister the classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # unregister the properties
    properties.unregister()
